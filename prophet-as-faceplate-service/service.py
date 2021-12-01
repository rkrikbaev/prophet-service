import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from modelInstances import ProphetModel

import os
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

def job(input_data:dict)->dict:

    start_time = time.ctime()

    metadata = input_data.get('metadata')

    settings = metadata.get('settings')
    point = metadata.get('point')
    history = input_data.get("history")
    future = input_data.get("future")
    
    inst = ProphetModel(settings, model_info=None)
        
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
    
    r, w = os.pipe()
        
    while True:

        response = {}

        try:
            with os.fdopen(r, "rb") as rf:
                
                content = rf.readline()
                data = json.loads(content)
            
                if {'metadata', 'history', 'future'} <= set(data):
                    response = job(input_data=data)
                    print(f'output {response}')
                else:
                    raise RuntimeError
        
        except Exception as exc:
            
            print(f'error{exc}')
        
        finally:
            
            with os.fdopen(w, "wb") as wf:
                wf.write(bytes(f'{response}\n',"UTF-8"))
