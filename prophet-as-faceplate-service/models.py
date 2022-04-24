"""
Classes for used models and algoritms

Class Prophet:

Prophet is a procedure for forecasting time series data based on 
an additive model where non-linear 
trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 
It works best with time series that have strong seasonal effects and several seasons of historical data. 
Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.


"""

from os import spawnlp
import pandas as pd

from prophet import Prophet

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProphetModel():

    def __init__(self, settings):

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
    def _create_prophet_df(self, data, columns):

        columns_size = len(columns) #2
        sample_size = len(data[0]) #5

        regressors_count = sample_size - columns_size

        # create "x_n" columns name for regressors
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
    def predict(self, history, future):

        response = {'state': 'error'}
     
        columns = ['ds']
        future = self._create_prophet_df(future, columns) # 2d array

        columns = ['ds', 'y']
        history = self._create_prophet_df(history, columns) # 2d array

        # add regressors to the model
        for item in future.columns:
            if item not in ['ds','y']:
                self.model.add_regressor(item)

        self.model.fit(history)
        response = self.model.predict(future)

        return response
    
    # find anomalies
    def anomalies(self, result)-> list:

        forecast = result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast.query('yhat_lower>yhat or yhat_upper<yhat', inplace=True)
        filtred_anomalies = forecast[['ds', 'yhat']]
        
        return filtred_anomalies.values.tolist()