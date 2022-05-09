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

    pc = Process()
    primary_keys = {'metadata', 'history', 'future'}
    
    pr = 3
    pw = 4

    rf = os.fdopen(pr)
    request = rf.readline()
    
    try:
        if bool(request):

            data = json.loads(request)
            logger.debug(f'incomming data {data}')

            if primary_keys <= set(data):
                response = pc.on_request(data)
                os.write(pw, bytes(f'{response}\n', "UTF-8"))  # 4
            else:
                raise RuntimeError(
                    'data must have METADATA, HISTORY and FUTURE fields')

    except RuntimeError as exc:
        logger.error(exc)
        sys.exit(1)
    
    sys.exit(0)