import falcon
from falcon.media.validators import jsonschema
from schemas import load_schema

from wsgiref.simple_server import make_server
import os

from resources.Predict import Predict
from logger import logger

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
cwd  = os.getcwd()

model_path = f'{cwd}/models' # path to saved Prophet's models

api = falcon.App()

api.add_route("/action", Predict())

if __name__ == "__main__":

    with make_server("", 8005, api) as httpd:
        logger.debug("Listening Port 8005...")
        # Serve until process is killed
        httpd.serve_forever()