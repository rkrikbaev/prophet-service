import logging
from logging.handlers import RotatingFileHandler
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
cwd  = os.getcwd()

log_path = f'{cwd}/logs/log.log'

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

# create console handler and set level to debug
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# create file handler and set level to debug
filelog = RotatingFileHandler(
    filename=f'{log_path}', 
    mode="a", 
    maxBytes=1024 * 1024
    )

filelog.setLevel(logging.DEBUG)

# add formatter
console.setFormatter(formatter)
filelog.setFormatter(formatter)

# add console to logger
logger.addHandler(console)

# add filelog to logger
logger.addHandler(filelog)
