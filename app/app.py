import falcon
from resources.service import Predict

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)

api = falcon.App()
api.add_route("/action", Predict())
logger.info('Server Loaded')
