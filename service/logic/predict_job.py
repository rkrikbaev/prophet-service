import pandas as pd
from datetime import datetime, date, time
import sys
import time
from logger import logger
from prophet import Prophet


class CallPredictAction():

    def __init__(self, settings, model_info=None):

        self.settings = settings
        # self.model_info = model_info

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

        # self.point = self.model_info["point"]
        # self.version = self.model_info["version"]
    
    def create_df(self, sample=None):

        _data = pd.DataFrame(data=sample)

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
            
            ## -- this logic must be implemented in OPERATOR

            # if (len(data.columns) - 1) == len(future.columns):
            #     pass
            # else:
            #     logger.info('History data columns must be more on one of regressor data')
            #     raise ValueError

            # if len(future.columns) > 1:

            #     hist_columns = ['ds','y']
            #     future_columns =[] 

            #     for index, item in enumerate(future.columns):
                    
            #         if index > 0:
            #             regressor_id = f'x_{index}'
            #             self.model.add_regressor(regressor_id)
            #             hist_columns.append(regressor_id)
            #             future_columns.append(regressor_id)
            #         else:
            #             future_columns.append('ds')

            #     future.columns = future_columns
            #     data.columns = hist_columns

            start_fit = int(time.time())
            self.model.fit(history)
            end_fit = int(time.time())

            logger.debug(f'fit time in: {end_fit - start_fit} seconds')
            
            forecast = self.model.predict(future)

            # response["predictions"] = forecast["yhat"].values.tolist()
            response["result"] = str(forecast.to_dict())
            response['state'] = {'status':'ok'}

        except Exception as e:
            logger.error(str(e))
        
        finally:
            return response