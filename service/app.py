import falcon
from falcon.media.validators import jsonschema
from schemas import load_schema

from wsgiref.simple_server import make_server
import os

from resources.Predict import Predict
from logger import logger

# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)
# cwd  = os.getcwd()

model_path = './model' # path to saved Prophet's models

api = falcon.App()

api.add_route("/action", Predict())

if __name__ == "__main__":

    app_port = os.getenv('APP_PORT', default=8005)

    with make_server("", int(app_port), api) as httpd:
        logger.debug("Listening Port 8005...")
        # Serve until process is killed
        httpd.serve_forever()
        