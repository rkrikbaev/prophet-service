import mlflow

from prophet.diagnostics import cross_validation, performance_metrics
from prophet import Prophet, serialize
# from prophet.serialize import model_to_json, model_from_json

import pandas as pd
import json
from middleware.logger import logger

"""
Class Prophet:

Prophet is a procedure for forecasting time series data based on 
an additive model where non-linear 
trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 
It works best with time series that have strong seasonal effects and several seasons of historical data. 
Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

"""
ARTIFACT_PATH = "model"

class ProphetModel():

    def __init__(self, settings):

        self.settings = settings

        self.model = Prophet(
            growth=self.settings["growth"],
            seasonality_mode=self.settings["seasonality_mode"],
            changepoint_prior_scale = self.settings['changepoint_prior_scale'], #30,
            seasonality_prior_scale = self.settings['seasonality_prior_scale'], #35,
            daily_seasonality = self.settings['daily_seasonality'],
            weekly_seasonality = self.settings['weekly_seasonality'], 
            yearly_seasonality = self.settings['yearly_seasonality'],                  
        )

        for season in self.settings['seasonality']:
            self.model.add_seasonality(
                name = season['name'],
                period = season['period'],
                fourier_order = season['fourier_order']
            )

        self.model_uri = None

    def call(self, history, future, model_uri) -> tuple:

        self.model_uri = model_uri

        if len(history[0]) <= len(future[0]):

            logger.warn('History data columns must include regressor data')
       
        else:

            history_columns = ['ds', 'y']
            future_columns = ['ds']

            additional_column_names = [f'x_{index}' for index, _ in enumerate(future[0]) if index > 0]
            
            history_columns.extend(additional_column_names)
            future_columns.extend(additional_column_names)

            for item in additional_column_names:
                self.model.add_regressor(item)
                
            if self.model_uri == None:
                
                df = self._process_data(
                data=history, columns=history_columns)
                self.model_uri = self.train(df=df)
            
            df = self._process_data(
                data=future,
                columns=future_columns)

            return self.predict(df), self.model_uri

    def train(self, df) -> dict:
        
        with mlflow.start_run():

            fitted_model = self.model.fit(df)
            mlflow.prophet.log_model(fitted_model, artifact_path=ARTIFACT_PATH)
            
            params = self.extract_params(fitted_model)

            metric_keys = ["mse", "rmse", "mae", "mape", "mdape", "smape", "coverage"]    
            cross_validation_params = self.settings.get('cross_validation')

            logger.debug(f'Cross validation params: {cross_validation_params}')
            
            cross_validation_enable = self.settings.get('cross_validation_enabled')

            if cross_validation_params and cross_validation_enable:
                metrics_raw = cross_validation(
                    model=fitted_model,
                    horizon=cross_validation_params.get('horizon'), # "365",
                    period=cross_validation_params.get('period'),  # "180",
                    initial=cross_validation_params.get('initial'),  # "710",
                    parallel=cross_validation_params.get('parallel'),  # "threads",
                    disable_tqdm=cross_validation_params.get('disable_tqdm'),  # True,
                    units=cross_validation_params.get('units') # days
                )

                cv_metrics = performance_metrics(metrics_raw)
                metrics = {k: cv_metrics[k].mean() for k in metric_keys}

                logger.debug(f"Logged Metrics: \n{json.dumps(metrics, indent=2)}")
                logger.debug(f"Logged Params: \n{json.dumps(params, indent=2)}")

                mlflow.log_metrics(metrics)
            
            mlflow.log_params(params)

            self.model_uri = mlflow.get_artifact_uri(ARTIFACT_PATH)
            
            logger.debug(f"Model artifact logged to: {self.model_uri}")

            return self.model_uri

    def predict(self, df) -> pd.DataFrame:

        loaded_model = mlflow.prophet.load_model(self.model_uri)

        forecast = loaded_model.predict(df)
        
        return forecast
        
    def _process_data(self, data, columns=None)->pd.DataFrame:

        df = None

        if len(data) == 0:
            raise RuntimeError
        
        else:
            
            df = pd.DataFrame(data)
            rename_columns = {index: x for index, x in enumerate(columns)}
            df.rename(columns=rename_columns, inplace=True)
               
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], unit='ms')
            df.reset_index(inplace=True, drop=True)

        return df

    def extract_params(self, pr_model):
        return {attr: getattr(pr_model, attr) for attr in serialize.SIMPLE_ATTRIBUTES} 
    # find anomalies
    def anomalies(self, result:pd.DataFrame, real_data:list) -> list:

        result['real'] = real_data
        forecast = result[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'real']]
        forecast.query('yhat_lower>real or yhat_upper<real', inplace=True)
        filtred_anomalies = forecast[['ds', 'yhat', 'real']]

        return filtred_anomalies.values.tolist()
