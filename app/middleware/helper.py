import logging, yaml, os, sys
import logging.config
from logging.handlers import RotatingFileHandler


# def logger(name='root', loglevel='INFO') -> None:
    
#     file_path = os.path.join(os.getcwd(), 'app/config/logger_config.yaml')
    

#     try:
#         with open(file_path, 'r') as fl:
#             config =  yaml.safe_load(fl)
#             logging.config.dictConfig(config) 
                       
#     except Exception as exc:
#         print(exc)

#     # formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    
#     # file_handler = logging.FileHandler('app/logs/app.log', mode='a', encoding=None, delay=False)

#     # file_handler.setLevel(logging.DEBUG)

#     # file_handler.setFormatter(formatter)

#     # logger = logging.getLogger(name) 
#     # logger.addHandler(file_handler)
    
#     logger = logging.getLogger(name)
    
#     return logger

def get_logger(name='root', loglevel='INFO'):
  
  logger = logging.getLogger(name)

  # if logger 'name' already exists, return it to avoid logging duplicate
  # messages by attaching multiple handlers of the same type
  if logger.handlers:
    return logger
  # if logger 'name' does not already exist, create it and attach handlers
  else:
    # set logLevel to loglevel or to INFO if requested level is incorrect
    loglevel = getattr(logging, loglevel.upper(), logging.INFO)
    logger.setLevel(loglevel)
    formate = '%(asctime)s [%(levelname)s] %(filename)-8s:: %(lineno)d : %(message)s'
    formate_date = '%Y-%m-%dT%T%Z'
    formatter = logging.Formatter(formate, formate_date)
    file_handler = RotatingFileHandler('./app/logs/app.log', mode='a', encoding=None, delay=False, maxBytes=5*1024*1024, backupCount=2)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if logger.name == 'root':
      logger.warning('Running: %s %s',
                     os.path.basename(sys.argv[0]),
                     ' '.join(sys.argv[1:]))
    return logger
