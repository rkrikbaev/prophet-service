import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
# import jsonschema
from schemas import load_schema
from modelInstance import CallPredictAction

import os
import time
import json
import sys

from logger import logger

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
    
    inst = CallPredictAction(settings, model_info=None)
        
    logger.debug("Call model")
    # Serve until model return response
    forecast = inst.run(history, future)
    anomalies_list = anomalies(forecast)

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

def anomalies(result)-> list:

    forecast = result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast.query('yhat_lower>yhat or yhat_upper<yhat', inplace=True)
    filtred_anomalies = forecast[['ds', 'yhat']]
    
    return filtred_anomalies.values.tolist()

if __name__ == "__main__":
    
    while True:
            
        body = input('Input: ')
        print(f'console: {body}')
        
        # pipe = os.fdopen(3)
        # body = pipe.readline()

        data = json.loads(body)
        
        if {'metadata', 'history', 'future'} <= set(data):
            
            response = job(input_data=data)
            logger.info(response)

            os.write(4, bytes(f'{response}\n',"UTF-8")) #4 
                
        else:

            time.sleep(5)
                    



    