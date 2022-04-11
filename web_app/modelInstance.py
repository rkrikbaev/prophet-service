# import pickle
# from xmlrpc.client import boolean
# from lib2to3.pgen2.pgen import DFAState
import mlflow

from prophet.diagnostics import cross_validation, performance_metrics
from prophet import Prophet, serialize
# from prophet.serialize import model_to_json, model_from_json

import pandas as pd
import json
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Model():

    def __init__(self, settings):

        self.settings = settings
        print('receive settings')

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

        self.model_available = False
        self.path = f'./model'
        self.save_model_after = False
        self.saved_model = None
        
        #if os.path.exists(self.path):
            
        #    self.model_available = self._load()
        #    self.save_model_after = True
    
    def call(self, func, history, future) -> dict:

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

            if func == 'train':

                df = self._process_data(
                    data=history, columns=history_columns)
                self.train(df=df)

            elif func == 'predict':

                df = self._process_data(
                    data=history, columns=history_columns)
                
                self.train(df=df)

                df = self._process_data(
                    data=future, columns=future_columns)
                
                return self.predict(df=df)
            
            else:

                logger.warn('Func was not selected')

    
    def train(self, df) -> dict:

        ARTIFACT_PATH = "model"
        
        with mlflow.start_run():

            model = self.model.fit(df)

            params = self.extract_params(model)

            # metric_keys = ["mse", "rmse", "mae", "mape", "mdape", "smape", "coverage"]
            # metrics_raw = cross_validation(
            #     model=model,
            #     horizon="365 days",
            #     period="180 days",
            #     initial="710 days",
            #     parallel="threads",
            #     disable_tqdm=True,
            # )

            # cv_metrics = performance_metrics(metrics_raw)
            # metrics = {k: cv_metrics[k].mean() for k in metric_keys}

            # print(f"Logged Metrics: \n{json.dumps(metrics, indent=2)}")
            print(f"Logged Params: \n{json.dumps(params, indent=2)}")

            mlflow.prophet.log_model(model, artifact_path=ARTIFACT_PATH)
            mlflow.log_params(params)
            # mlflow.log_metrics(metrics)

            self.model_uri = mlflow.get_artifact_uri(ARTIFACT_PATH)
            print(f"Model artifact logged to: {self.model_uri}")

    def predict(self, df) -> dict:

        loaded_model = mlflow.prophet.load_model(self.model_uri)

        forecast = loaded_model.predict(df)

        print(f"forecast:\n${forecast.head(30)}")
        
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
