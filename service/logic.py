import pandas as pd
from datetime import datetime, date, time
import sys
import time
from logger import logger
from prophet import Prophet


class CallPredictAction():

    def __init__(self, settings, model_info=None):

        self.settings = settings

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
    
    def create_df(self, sample):

        _data = pd.DataFrame(sample.get('data'),columns=sample.get('columns'))

        if len(_data) == 0:
            logger.info('Dataset cannot be empty')
            raise ValueError
        else:       

            _data[_data.columns[0]] = pd.to_datetime(_data[_data.columns[0]], unit='ms')
            _data.reset_index(inplace=True, drop=True)

            return _data

    def job(self, history, future):

        response = {}
        response['state'] = {'status': 'error'}

        try:       

            future = self.create_df(future) # 2d array
            history = self.create_df(history) # 2d array

            for item in future.columns:
                if item not in ['ds','y']:
                    self.model.add_regressor(item)

            self.model.fit(history)
            
            forecast = self.model.predict(future)

            response["result"] = str(forecast.to_dict())
            response['prediction'] = forecast['yhat'].values.tolist()
            response['state'] = {'status':'ok'}

        except Exception as e:
            logger.error(str(e))
        
        finally:
            return response