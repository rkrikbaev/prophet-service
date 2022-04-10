# import pickle
# from xmlrpc.client import boolean
import pandas as pd
from datetime import datetime, date, time

from logger import logger
from prophet import Prophet

from prophet.serialize import model_to_json, model_from_json
import json
import os


class Model():

    def __init__(self, settings):

        self.settings = settings
        print('receive settings')

        self.model = Prophet(
            growth = settings["growth"],
            seasonality_mode = "multiplicative",
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
        
        if os.path.exists(self.path):
            
            self.model_available = self._load()
            self.save_model_after = True

    def predict(self, history_data, regression) -> dict:
        
        """
        [Main flow fit/train and predict]

        Args:
            history (2Darray): [History data fit model]
            future (2Darray): [Future dataset]

        Returns:
            dict:[return result of prediction as dict with fields: result, prediction, state]

        """

        data_columns = ['ds', 'y']
        regression_columns = ['ds']

        # how_many_elements_in_regression = len(regression[0])

        if len(history_data[0]) <= len(regression[0]):

            logger.error('History data columns must include regressor data')
            raise RuntimeError

        regressor_names = [
            f'x_{index}' for index, _ in enumerate(regression[0]) if index > 0]
        
        data_columns.extend(regressor_names)
        regression_columns.extend(regressor_names)

        df_data = self._process_data(
            data=history_data,
            columns=data_columns
        )

        df_resression = self._process_data(
            data=regression,
            columns=regression_columns
        )     

        for item in regressor_names:
            self.model.add_regressor(item)
        
        if self.model_available:

            self.model.fit(df_data, init=self._stan_init(m=self.saved_model))

        else:
            
            self.model.fit(df_data)
        
        if self.save_model_after:
            self._save()
        
        response = self.model.predict(df_resression)
        
        return response
        
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

    def _save(self) -> bool:

        logger.debug('try to save model')
        
        if os.path.exists(self.path):
            with open(f'{self.path}/model.json', 'w') as fout:
                json.dump(model_to_json(self.model), fout)  # Save model
                logger.debug('model saved')
                return True
        else:
            logger.info(f'Cannot save the model')
  
    def _load(self) -> bool:
        
        logger.debug('try to load model')
        
        path = f'{self.path}/model.json'
        print(path)

        if os.path.exists(path):
            with open(path, 'r') as fin:
                self.saved_model = model_from_json(
                    json.load(fin))  # Load model
                logger.debug('model loaded')
                return True
        else:        
            logger.info(f'Model {path} not exist')
            return False

    def _stan_init(self, m):

        """Retrieve parameters from a trained model.
        
        Retrieve parameters from a trained model in the format
        used to initialize a new Stan model.
        
        Parameters
        ----------
        m: A trained model of the Prophet class.
        
        Returns
        -------
        A Dictionary containing retrieved parameters of m.
        
        """
        params = {}

        if m is None:
            return None
        else:

            print(m.params)
        
            for pname in ['k', 'm', 'sigma_obs']:
                params[pname] = m.params[pname][0][0]
            for pname in ['delta', 'beta']:
                params[pname] = m.params[pname][0]
        
        return params
