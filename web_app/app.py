import falcon
from resources.service import Predict

from middleware.logger import logger

api = falcon.App()
api.add_route("/action", Predict())
logger.info('Server Loaded')
