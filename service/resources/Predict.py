import falcon
from falcon.media.validators import jsonschema

import datetime
import time

from logger import logger
from schemas import load_schema
from logic.predict_job import CallPredictAction

# Make prediction
class Predict:

    def __init__(self, cfg=None):
        self.cfg = cfg
    
    def on_get(self, req, resp):
        resp.media = "ok"

    @jsonschema.validate(req_schema=load_schema('request'))
    def on_post(self, req, resp):

        resp.status = falcon.HTTP_400
        data =  req.media

        # model = data["model"]
        settings = data["settings"]
        history = data["history"]
        future = data["future"]

        try:
            paction = CallPredictAction(settings)
            resp.media = paction.job(history, future)
            resp.status = falcon.HTTP_201
        
        except Exception as error:
            logger.error(error)
            resp.status = falcon.HTTP_500