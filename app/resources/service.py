import sys
from falcon.media.validators import jsonschema
from schemas import load_schema
from models import ProphetModel
import json
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)


# Make prediction
class Predict:
    
    def on_get(self, req, resp):
        resp.media = "ok"

    @jsonschema.validate(req_schema=load_schema('request'))
    def on_post(self, req, resp):

        data = {
            "settings": [],
            "features": [],
            "history": [],
            "regression": []
        }
        
        data =  req.media

        logger.debug(f'Incomming data: {list(data.keys())}')
        
        settings = json.loads(data["settings"])
        features = data["features"]
        history_data = data["history"]
        future_data = data["future"]
        model_uri = data.get("model_uri")

        model = ProphetModel(settings)

        forecast, model_uri = model.call(
            history_data, future_data, model_uri)
        response = self._filter_response(forecast, features)
        response["model_uri"] = model_uri
        logger.debug(f'Outgoing data keys: {list(response.keys())}')
        logger.debug(f'Outgoing data: {response}')
        resp.media = response

    def _filter_response(self, forecast, features)->dict:
        
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