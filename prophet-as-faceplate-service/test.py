import pandas as pd
from models import ProphetModel
from datetime import datetime
import json
import logging
import sys
import os
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)
pd.options.mode.chained_assignment = None  # default='warn'


class Process:

    def __init__(self):
        self.response = {}

    def on_request(self, data: dict) -> dict:
        metadata = data.get('metadata')
        point = metadata.get('point')
        
        history_data = data.get("history")
        future_data = data.get("future")
        settings = metadata.get('settings')
        features = metadata.get('features')
        model_uri = metadata.get('model_uri')

        start_time = str(datetime.now())

        model = ProphetModel(settings)
        forecast, _anomalies, model_uri = model.call(
            history_data, future_data, model_uri)

        stop_time = str(datetime.now())

        self.response['metadata'] = {
            'start_time': start_time,
            'stop_time': stop_time,
            'point': point,
            "model_uri": model_uri if model_uri else None
        }

        self.response = self._filter_response(forecast, features)
        
        _anomalies = [int(x[0].timestamp())
                      for x in _anomalies]

        self.response["anomalies"] = _anomalies
        self.response['prediction'] = self.response['yhat']
        # del self.response['yhat']

        logger.debug(f'outgoing data {self.response}')

        return self.response

    def _filter_response(self, forecast, features) -> dict:

        for item in features:
            if item in forecast:
                self.response[item] = forecast[item].values.tolist()
            else:
                logger.info('key not exist')
        return self.response

if __name__ == "__main__":

    start_time = str(datetime.today())
    request = '''
            {
                "future":[[1641315208964,10.409359306702795],[1641315268964,10.326631842096198],[1641315328964,10.154809696155231],[1641315388964,10.480855760835036],[1641315448964,10.187294774862359],[1641315508964,10.336809843405321],[1641315568964,10.445442408449246],[1641315628964,10.116806437647783],[1641315688964,10.409785188367287],[1641315748964,10.324862581103021],[1641315808964,10.155365128990237],[1641315928964],[1641315988964],[1641316048964],[1641316108964],[1641316168964],[1641316228964],[1641316288964],[1641316348964],[1641316408964],[1641316468964],[1641316528964],[1641316588964],[1641316648964],[1641316708964],[1641316768964],[1641316828964],[1641316888964],[1641316948964],[1641317008964],[1641317068964],[1641317128964],[1641317188964],[1641317248964],[1641317308964],[1641317368964],[1641317428964],[1641317488964],[1641317548964],[1641317608964]],
                "history":[[1641312268964,10.119494279320358],[1641312328964,10.411538122078568],[1641312388964,10.32504137623092],[1641312448964,10.153973212878418],[1641312508964,10.48020110073652],[1641312568964,9.869381359161531],[1641312628964,10.274620191371469],[1641312688964,10.44595137847908],[1641312748964,10.520537468206047],[1641312808964,10.41163617634976],[1641312868964,10.217450926962767],[1641312928964,10.154699237739337],[1641312988964,10.482430857060454],[1641313048964,10.18853778198251],[1641313108964,10.27577774600039],[1641313168964,10.445234243921089],[1641313228964,10.221683466851955],[1641313288964,10.415114334050273],[1641313348964,10.32535467074065],[1641313408964,10.153807424932486],[1641313468964,10.482869277142955],[1641313528964,10.191971679190468],[1641313588964,10.530859836430698],[1641313648964,10.445581011403114],[1641313708964,10.118026941329877],[1641313768964,10.410396968017016],[1641313828964,10.3248452960751],[1641313888964,9.907832277672137],[1641313948964,10.482509688690865],[1641314008964,10.189235047265566],[1641314068964,10.273719724253333],[1641314128964,10.445079292324335],[1641314188964,10.11926020771186],[1641314248964,10.41116353738899],[1641314308964,10.25555012411867],[1641314368964,10.155641101609445],[1641314428964,10.483117757462269],[1641314488964,10.188695328088997],[1641314548964,10.2757903181135],[1641314608964,10.444745593441922],[1641314668964,10.11958896085127],[1641314728964,10.67748263101912],[1641314788964,10.324892257486171],[1641314848964,10.153948351826617],[1641314908964,10.481575607055905],[1641314968964,10.189324822673155],[1641315028964,10.274724257149249],[1641315088964,10.440840635174862],[1641315148964,10.394818550541912],[1641315208964,10.409359306702795],[1641315268964,10.326631842096198],[1641315328964,10.154809696155231],[1641315388964,10.480855760835036],[1641315448964,10.187294774862359],[1641315508964,10.336809843405321],[1641315568964,10.445442408449246],[1641315628964,10.116806437647783],[1641315688964,10.409785188367287],[1641315748964,10.324862581103021],[1641315808964,10.155365128990237]],
                "metadata":{
                    "point": "shym-2", 
                    "type": "",
                    "model_uri": "file:///Users/rustamkrikbayev/prophet-service/mlruns/0/d3029c49379648eaac3ea131c6c4c7a9/artifacts/model",
                    "features": ["yhat","yhat_lower","yhat_upper"],
                    "settings":{
                        "growth": "linear",
                        "seasonality_mode": "multiplicative",
                        "changepoint_prior_scale": 30,
                        "seasonality_prior_scale": 35,
                        "interval_width": 0.98,
                        "daily_seasonality": false,
                        "weekly_seasonality": false,
                        "yearly_seasonality": false,
                        "seasonality": [{
                            "name": "hour","period": 0.0417,
                            "fourier_order": 5}]
                        }
                    }
                }
    '''

    pc = Process()
    primary_keys = {'metadata', 'history', 'future'}

    pr = 3
    pw = 4

    rf = os.fdopen(pr)
    # request = rf.readline()

    try:
        if bool(request):

            data = json.loads(request)
            logger.debug(f'incomming data {data}')

            if primary_keys <= set(data):
                response = pc.on_request(data)
                # os.write(pw, bytes(f'{response}\n', "UTF-8"))  # 4
            else:
                raise RuntimeError(
                    'data must have METADATA, HISTORY and FUTURE fields')

    except RuntimeError as exc:
        logger.error(exc)
        sys.exit(1)

    sys.exit(0)
