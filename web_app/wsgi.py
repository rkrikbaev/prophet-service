from app import api

import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# --------- For local debugging/test only ----------
from wsgiref.simple_server import make_server

if __name__ == "__main__":

    app_port = os.getenv('APP_PORT', default=8005)

    with make_server("", int(app_port), api) as httpd:
        logger.debug("Listening Port 8005...")
        # Serve until process is killed
        httpd.serve_forever()
# --------- For local debugging/test only ----------
