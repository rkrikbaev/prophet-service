"""
    Class Prophet:
    
    Prophet is a procedure for forecasting time series data based on 
    an additive model where non-linear 
    trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 
    It works best with time series that have strong seasonal effects and several seasons of historical data. 
    Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

"""
import json
import pandas as pd
from prophet import Prophet, serialize
from prophet.diagnostics import cross_validation, performance_metrics
import mlflow
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)
# import holidays as holidays

ARTIFACT_PATH = "model"


class ProphetModel():

    def __init__(self, settings):

        self.settings = settings

        self.model = Prophet(
            growth=self.settings["growth"],
            seasonality_mode=self.settings["seasonality_mode"],
            changepoint_prior_scale=self.settings['changepoint_prior_scale'],
            seasonality_prior_scale=self.settings['seasonality_prior_scale'],
            daily_seasonality=self.settings['daily_seasonality'],
            weekly_seasonality=self.settings['weekly_seasonality'],
            yearly_seasonality=self.settings['yearly_seasonality']
            # holidays=pd.DataFrame(sorted(holidays.KZ(
            #     years=[2022]).items()), columns=['ds', 'holiday'])
        )

        for season in self.settings['seasonality']:
            self.model.add_seasonality(
                name=season['name'],
                period=season['period'],
                fourier_order=season['fourier_order']
            )

    def call(self, history, future, model_uri) -> tuple:
        self.model_uri = model_uri
        regressor_names = [f'x_{index-2}' for index, _ in enumerate(
            history[0]) if index > 1]
        for item in regressor_names:
            self.model.add_regressor(item)
        while True:
            if self.model_uri is None or self.model_uri.find('artifacts/model') == -1:
                logger.debug('train branch')
                _columns = ['ds', 'y']
                _columns.extend(regressor_names)
                df = self._process_data(
                    data=history, columns=_columns)
                self.model_uri = self.train(df)
            else:
                logger.debug('predict branch')
                _columns = ['ds']
                _columns.extend(regressor_names)
                df = self._process_data(
                    data=future,
                    columns=_columns)
                _predict = self.predict(df)
                _anomalies = self.anomalies(
                    result=_predict, real_data=future)
                return _predict, _anomalies, self.model_uri

    def train(self, df) -> dict:

        with mlflow.start_run():

            fitted_model = self.model.fit(df)
            mlflow.prophet.log_model(fitted_model, artifact_path=ARTIFACT_PATH)

            params = self.extract_params(fitted_model)

            metric_keys = ["mse", "rmse", "mae",
                           "mape", "mdape", "smape", "coverage"]
            cross_validation_params = self.settings.get('cross_validation')

            logger.debug(f'Cross validation params: {cross_validation_params}')

            cross_validation_enable = self.settings.get(
                'cross_validation_enabled')

            if cross_validation_params and cross_validation_enable:
                metrics_raw = cross_validation(
                    model=fitted_model,
                    horizon=cross_validation_params.get('horizon'),  # "365",
                    period=cross_validation_params.get('period'),  # "180",
                    initial=cross_validation_params.get('initial'),  # "710",
                    parallel=cross_validation_params.get(
                        'parallel'),  # "threads",
                    disable_tqdm=cross_validation_params.get(
                        'disable_tqdm'),  # True,
                    units=cross_validation_params.get('units')  # days
                )

                cv_metrics = performance_metrics(metrics_raw)
                metrics = {k: cv_metrics[k].mean() for k in metric_keys}

                logger.debug(
                    f"Logged Metrics: \n{json.dumps(metrics, indent=2)}")
                logger.debug(
                    f"Logged Params: \n{json.dumps(params, indent=2)}")

                mlflow.log_metrics(metrics)

            mlflow.log_params(params)

            self.model_uri = mlflow.get_artifact_uri(ARTIFACT_PATH)

            logger.debug(f"Model artifact logged to: {self.model_uri}")

            return self.model_uri

    def predict(self, df) -> pd.DataFrame:

        loaded_model = mlflow.prophet.load_model(self.model_uri)

        forecast = loaded_model.predict(df)

        return forecast

    def _process_data(self, data, columns) -> pd.DataFrame:

        df = pd.DataFrame(data)
        rename_columns = {index: x for index, x in enumerate(columns)}
        df.rename(columns=rename_columns, inplace=True)
        _df = df[columns].copy()
        _df[_df.columns[0]] = pd.to_datetime(_df[_df.columns[0]], unit='ms')
        _df.reset_index(inplace=True, drop=True)

        return _df

    def extract_params(self, pr_model):
        return {attr: getattr(pr_model, attr) for attr in serialize.SIMPLE_ATTRIBUTES}

    def anomalies(self, result: pd.DataFrame, real_data) -> list:

        df = pd.DataFrame(data=real_data)
        result['real'] = df[df.columns[1]]

        forecast = result[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'real']]

        forecast.query('yhat_lower>real or yhat_upper<real', inplace=True)
        filtred_anomalies = forecast[['ds', 'yhat', 'real']]

        return filtred_anomalies.values.tolist()