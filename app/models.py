"""
    Class Prophet:
    
    Prophet is a procedure for forecasting time series data based on 
    an additive model where non-linear 
    trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 
    It works best with time series that have strong seasonal effects and several seasons of historical data. 
    Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

"""
import pandas as pd
from prophet import Prophet, serialize
from prophet.diagnostics import cross_validation, performance_metrics
import mlflow

from middleware.helper import get_logger
logger = get_logger(__name__, loglevel='DEBUG')

tracking_server_uri = "http://127.0.0.1:5000"  # set to your server URI

try:
    mlflow.set_tracking_uri(tracking_server_uri)
except:
    logger.error(
        """Couldn't connect to remote MLFLOW tracking server""")

class ProphetModel():

    def __init__(self):
        self.response = {} 
        self.anomalies = []

    def run(self, data, model_uri):

        future = data.get('future')
        regressor_names = data.get('regressor_names')
        features = data.get('features')

        if model_uri is None or model_uri.find('artifacts/model') == -1:
            logger.debug('There is no path to the model')
            raise RuntimeError('There is no path to the model')
        else:
            model = mlflow.prophet.load_model(model_uri)
            logger.debug('Preprocess data for a predict')
            columns = ['ds']
            columns.extend(regressor_names)
            
            data = self._process_data(
                data=future,
                columns=columns)

            result = model.predict(data)

            self.anomalies = self.find_anomalies(
                result, real_data=future)

            self.response = self._filter_response(result, features)

        return self.response, self.anomalies

    def _process_data(self, data, columns) -> pd.DataFrame:

        df = pd.DataFrame(data)
        rename_columns = {index: x for index, x in enumerate(columns)}
        df.rename(columns=rename_columns, inplace=True)
        _df = df[columns].copy()
        _df[_df.columns[0]] = pd.to_datetime(_df[_df.columns[0]], unit='ms')
        _df.reset_index(inplace=True, drop=True)

        return _df

    def find_anomalies(self, result: dict, real_data) -> list:

        df = pd.DataFrame(data=real_data)
        
        result['real'] = df[df.columns[1]]

        forecast = result[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'real']]
        forecast.query('yhat_lower>real or yhat_upper<real', inplace=True)
        forecast['ds'] = forecast[['ds']].astype('int64') // 10**9
        
        return forecast[['ds', 'real']].values.tolist()
    
    def _filter_response(self, forecast, features) -> dict:

        response = {}

        if forecast is None:
            return response

        try:
            for item in features:
                try:
                    if item in forecast:
                        response[item] = forecast[item].values.tolist()
                    else:
                        logger.info('key not exist')
                except Exception as exc:
                    logger.error(exc)
        except:
            pass

        return response

    def train():
        pass