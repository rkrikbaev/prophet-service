from app import api
import os

from middleware.helper import get_logger
logger = get_logger(__name__, loglevel='DEBUG')

# --------- For local debugging/test only ----------
from wsgiref.simple_server import make_server

if __name__ == "__main__":

    app_port = os.getenv('APP_PORT', default=8005)

    with make_server("", int(app_port), api) as httpd:
        logger.debug(f"Listening Port {app_port}...")
        # Serve until process is killed
        httpd.serve_forever()
# --------- For local debugging/test only ----------

