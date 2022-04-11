import falcon
from resources.model import Predict

import logging, os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# --------- For local debugging/test only ----------
# from wsgiref.simple_server import make_server
# --------- For local debugging/test only ----------

api = falcon.App()
api.add_route("/action", Predict())
logger.info('Server Loaded')

# --------- For local debugging/test only ----------
# if __name__ == "__main__":

#     app_port = os.getenv('APP_PORT', default=8005)

#     with make_server("", int(app_port), api) as httpd:
#         logger.debug("Listening Port 8005...")
#         # Serve until process is killed
#         httpd.serve_forever()
# --------- For local debugging/test only ----------
