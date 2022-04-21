import falcon
from resources.model import Predict

import logging, os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

api = falcon.App()
api.add_route("/action", Predict())
logger.info('Server Loaded')
