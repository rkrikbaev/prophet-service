import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from modelInstances import ProphetInst

import os, sys
import time
import json

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# add formatter
console.setFormatter(formatter)

# add console to logger
logger.addHandler(console)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
cwd  = os.getcwd()

model_path = f'{cwd}/models' # path to saved Prophet's models

def send_to(fd, message):

    try:
        print("writing: ", message)
        os.write(fd, bytes(f'{message}\n',"UTF-8")) #4
    except Exception as err:
        time.sleep(10)

def job(input_data:dict)->dict:

    start_time = time.ctime()

    metadata = input_data.get('metadata')

    settings = metadata.get('settings')
    point = metadata.get('point')
    history = input_data.get("history")
    future = input_data.get("future")
    
    inst = ProphetInst(settings, model_info=None)
        
    forecast = inst.run(history, future)
    anomalies_list = inst.anomalies(forecast)

    finish_time = time.ctime()

    response_body = {
            "metadata": {
                "point": point,
                "start_time": start_time,
                "finish_time": finish_time
                },
            "prediction": forecast['yhat'].values.tolist(),
            "anomalies": anomalies_list
            }

    return response_body

if __name__ == "__main__":
    
    
    pw = os.open("pipeFrom", os.O_WRONLY | os.O_CREAT)
    
    try:
        pr = os.open("pipeTo", os.O_RDONLY)
    except FileNotFoundError as exc:
        logger.error(exc)
        sys.exit(1)

    try:
        with os.fdopen(pr, "rb") as rf:
            content = rf.read()
    except OSError as exc:
        logger.error(exc)
        sys.exit(1)

    try:
            
        if bool(content):

            data = json.loads(content)

            logger.debug(f'received data {data}')
        
            if {'metadata', 'history', 'future'} <= set(data):
                response = job(input_data=data)
                send_to(pw, message=response)
                logger.debug(response)

            else:
                logger.info('data must have METADATA, HISTORY, FUTURE fields')
        else:
            logger.info('file is empty')
    except Exception as exc:
        
        logger.error(exc)

    sys.exit(0)

