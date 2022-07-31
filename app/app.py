import falcon
from falcon.media.validators import jsonschema

from schemas import load_schema
from models import ProphetModel

from middleware.helper import get_logger
logger = get_logger(__name__, loglevel='DEBUG')

class CheckHealth():

    def on_get(self, req, resp):
        resp.media = "ok"

class Predict:

    # @jsonschema.validate(req_schema=load_schema('request'))
    def on_post(self, req, resp):
        response = {}
        data = req.media

        model_uri = data.get('model_uri')

        model = ProphetModel()

        predict, anomalies = model.run(data, model_uri)
        
        response["model_uri"] = model_uri
        response["anomalies"] = anomalies
        response["prediction"] = predict

        logger.debug(f'Outgoing data keys: {list(response.keys())}')
        logger.debug(f'Outgoing data: {response}')

        resp.media = response

api = falcon.App()

api.add_route("/health", CheckHealth())
api.add_route("/action", Predict())

logger.info("Server Loaded")