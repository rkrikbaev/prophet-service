import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from models import ProphetModel

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
filePath = cwd
nodeName = ''

logger.debug(filePath)

try:
   nodeName = sys.argv[1]
except:
   pass

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

    model = ProphetModel(settings, model_info=None)

    forecast = model.run(history, future)
    anomalies_list = model.anomalies(forecast)

    finish_time = time.ctime()
    
    try:

        features = data.get('features')

        for item in features:
            try:
                if item in forecast:
                    response[item] = forecast[item].values.tolist()
                else:
                    logger.info('name not exist')
            except Exception as exc:
                logger.error(exc)
    except:
        pass
    
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

    # JSON = '''
    # {"future":[[1641315928964],[1641315988964],[1641316048964],[1641316108964],[1641316168964],[1641316228964],[1641316288964],[1641316348964],[1641316408964],[1641316468964],[1641316528964],[1641316588964],[1641316648964],[1641316708964],[1641316768964],[1641316828964],[1641316888964],[1641316948964],[1641317008964],[1641317068964],[1641317128964],[1641317188964],[1641317248964],[1641317308964],[1641317368964],[1641317428964],[1641317488964],[1641317548964],[1641317608964]],
    # "history":[[1641312268964,10.119494279320358],[1641312328964,10.411538122078568],[1641312388964,10.32504137623092],[1641312448964,10.153973212878418],[1641312508964,10.48020110073652],[1641312568964,9.869381359161531],[1641312628964,10.274620191371469],[1641312688964,10.44595137847908],[1641312748964,10.520537468206047],[1641312808964,10.41163617634976],[1641312868964,10.217450926962767],[1641312928964,10.154699237739337],[1641312988964,10.482430857060454],[1641313048964,10.18853778198251],[1641313108964,10.27577774600039],[1641313168964,10.445234243921089],[1641313228964,10.221683466851955],[1641313288964,10.415114334050273],[1641313348964,10.32535467074065],[1641313408964,10.153807424932486],[1641313468964,10.482869277142955],[1641313528964,10.191971679190468],[1641313588964,10.530859836430698],[1641313648964,10.445581011403114],[1641313708964,10.118026941329877],[1641313768964,10.410396968017016],[1641313828964,10.3248452960751],[1641313888964,9.907832277672137],[1641313948964,10.482509688690865],[1641314008964,10.189235047265566],[1641314068964,10.273719724253333],[1641314128964,10.445079292324335],[1641314188964,10.11926020771186],[1641314248964,10.41116353738899],[1641314308964,10.25555012411867],[1641314368964,10.155641101609445],[1641314428964,10.483117757462269],[1641314488964,10.188695328088997],[1641314548964,10.2757903181135],[1641314608964,10.444745593441922],[1641314668964,10.11958896085127],[1641314728964,10.67748263101912],[1641314788964,10.324892257486171],[1641314848964,10.153948351826617],[1641314908964,10.481575607055905],[1641314968964,10.189324822673155],[1641315028964,10.274724257149249],[1641315088964,10.440840635174862],[1641315148964,10.394818550541912],[1641315208964,10.409359306702795],[1641315268964,10.326631842096198],[1641315328964,10.154809696155231],[1641315388964,10.480855760835036],[1641315448964,10.187294774862359],[1641315508964,10.336809843405321],[1641315568964,10.445442408449246],[1641315628964,10.116806437647783],[1641315688964,10.409785188367287],[1641315748964,10.324862581103021],[1641315808964,10.155365128990237]],
    # "metadata":{"changepoint_prior_scale":30,"daily_seasonality":false,"growth":"linear","interval_width":0.98,"seasonality":[{"fourier_order":5,"name":"hour","period":0.0417}],"seasonality_prior_scale":35,"weekly_seasonality":false,"yearly_seasonality":false}
    # }
    # '''

    # with point, type
    # JSON = '''{
    #     "metadata": { "point": "shym-2","type": "prophet","settings":{"growth": "linear","changepoint_prior_scale": 30,"seasonality_prior_scale": 35,"interval_width": 0.98,"daily_seasonality": false,"weekly_seasonality": false,"yearly_seasonality": false,"seasonality": [{"name": "hour","period": 0.0417,"fourier_order": 5}]}},
    #     "history": [[1626159114000, 46.46659429239697, 33.865], [1626162714000, 50.38077545566983, 33.135], [1626166314000, 49.786295583493974, 33.0], [1626169914000, 52.30600325119654, 33.0], [1626173514000, 49.74017713527362, 32.135], [1626177114000, 26.507367125644155, 32.0], [1626180714000, 20.825400896539158, 31.135], [1626184314000, 16.641573343804414, 30.135], [1626187914000, 12.88365472938776, 28.27], [1626191514000, 13.03941161652353, 27.135], [1626195114000, 12.865383213700188, 26.135], [1626198714000, 23.0075885798094, 26.0], [1626202314000, 29.750946025369963, 26.0], [1626205914000, 30.36831248536057, 25.135], [1626209514000, 28.746051325005425, 24.135], [1626213114000, 26.06918637600051, 23.135], [1626216714000, 27.71889996848636, 23.0], [1626220314000, 27.61792646200975, 23.0], [1626223914000, 29.282521453022955, 22.135], [1626227514000, 27.6570642212926, 24.595], [1626231114000, 29.47211756398148, 26.73], [1626234714000, 20.901465210812887, 28.73], [1626238314000, 19.566893250178232, 29.865], [1626241914000, 20.06650195276843, 30.865], [1626245514000, 19.581432925954925, 31.0], [1626249114000, 19.763265444149177, 31.865], [1626252714000, 20.146312865931193, 32.865], [1626256314000, 19.499077251661088, 33.865], [1626259914000, 20.496050887058047, 33.135], [1626263514000, 19.918877556726137, 33.0], [1626267114000, 19.885642845565478, 32.135], [1626270714000, 14.614254379067686, 31.135], [1626274314000, 12.052995100595156, 30.135], [1626277914000, 12.075608591365814, 29.135], [1626281514000, 11.714862450722588, 27.27], [1626285114000, 22.17041537279129, 24.405], [1626288714000, 29.7315270995956, 22.27], [1626292314000, 27.034812883857093, 21.135], [1626295914000, 30.357443650132815, 19.27], [1626299514000, 30.623968757263288, 19.0], [1626303114000, 29.982753248142135, 18.135], [1626306714000, 30.91508703640832, 18.0], [1626310314000, 31.083123297907484, 17.135], [1626313914000, 32.9891217580737, 17.0], [1626317514000, 28.84762504017565, 20.46], [1626321114000, 25.25211722192711, 21.0041067761807], [1626324714000, 23.6941498622534, 20.46], [1626328314000, 22.01953280939939, 10]],
    #     "future": [[1626321114000, 19.27],[1626321115000, 19.27],[1626321116000, 66.1]]
    #     }'''

    # pr,pw = os.pipe()
    # print(pr,pw)
    # message = JSON.replace("\n", "") + "\n"
    # writesBytes = os.write(pw, bytes(message, 'utf-8'))
    
    pr = 3
    pw = 4
    rf = os.fdopen(pr)
    content = rf.readline()

    # try:
    #     with os.fdopen(3, "rb") as rf:
    #         content = rf.readline()
    #         print(content)
    # except OSError as exc:
    #     logger.error(exc)
    #     sys.exit(1)s
    
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