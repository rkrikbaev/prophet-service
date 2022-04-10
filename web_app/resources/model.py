import falcon
from falcon.media.validators import jsonschema

from logger import logger
from schemas import load_schema
from modelInstance import Model

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
        
        resp.status = falcon.HTTP_400
        data =  req.media

        logger.debug(data)
        
        settings = data["settings"]
        features = data["features"]
        history_data = data["data"]
        regression_data = data["regression"]

        model = Model(settings)

        forecast = model.predict(
            history_data, regression=regression_data
            )

        resp.media = self._filter_response(forecast, features)
        resp.status = falcon.HTTP_201
        logger.debug('Succesefull response')

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