from app import api
import os, sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)

# --------- For local debugging/test only ----------
from wsgiref.simple_server import make_server

if __name__ == "__main__":

    app_port = os.getenv('APP_PORT', default=8005)

    with make_server("", int(app_port), api) as httpd:
        logger.debug(f"Listening Port {app_port}...")
        # Serve until process is killed
        httpd.serve_forever()
# --------- For local debugging/test only ----------

