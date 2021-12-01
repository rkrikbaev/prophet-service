from os import spawnlp
import pandas as pd
from logger import logger
from prophet import Prophet


class ProphetModel():

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
    
    # prepare data for fitting
    def create_prophet_df(self, data, columns):

        columns_size = len(columns) #2
        sample_size = len(data[0]) #5

        regressors_count = sample_size - columns_size

        for item in range(0,regressors_count):
            columns.append(f'x_{item+1}')


        _data = pd.DataFrame(data=data,columns=columns)

        if len(_data) == 0:
            logger.info('Dataset cannot be empty')
            raise ValueError
        else:       

            _data[_data.columns[0]] = pd.to_datetime(_data[_data.columns[0]], unit='ms')
            _data.reset_index(inplace=True, drop=True)

            return _data
    
    # fit model and get prediction
    def run(self, history, future):

        response = {}
        response['state'] = {'status': 'error'}

        try:       
            columns = ['ds']
            future = self.create_prophet_df(future, columns) # 2d array

            columns = ['ds', 'y']
            history = self.create_prophet_df(history, columns) # 2d array

            for item in future.columns:
                if item not in ['ds','y']:
                    self.model.add_regressor(item)

            self.model.fit(history)
            
            forecast = self.model.predict(future)

        except Exception as e:
            logger.error(str(e))
        
        finally:
            return forecast
    
    # find anomalies
    def anomalies(self, result)-> list:

        forecast = result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast.query('yhat_lower>yhat or yhat_upper<yhat', inplace=True)
        filtred_anomalies = forecast[['ds', 'yhat']]
        
        return filtred_anomalies.values.tolist()