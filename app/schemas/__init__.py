import os
import sys
import json
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)

def load_schema(name):
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{}.json'.format(name))

    with open(os.path.abspath(path), 'r') as fp:
        data = fp.read()
    return json.loads(data)