import os
import logging
import sys
import time
import platform
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
# from safety.business_logics.config.properties import LOG_DIRECTORY, LOG_FILE
import json
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import timedelta
FORMATTER = logging.Formatter("%(threadName)s %(asctime)s  %(name)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s")


LOG_DIRECTORY = None
LOG_FILE = 'NLP_ML'
log_path_details = None


LOG_DIRECTORY = "./logs"

print("LOG_DIRECTORY","\t****"*10,LOG_DIRECTORY)

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler():
#    file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIRECTORY, LOG_FILE), when='midnight')
   file_handler =  RotatingFileHandler(os.path.join(LOG_DIRECTORY,LOG_FILE +time.strftime('-%Y-%m-%d')+".log"),backupCount=50,maxBytes=10000000)
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger
   
mylogger = get_logger(__name__)
mylogger.info("Created logger")


def test(i):
       time.sleep(1)
      #  mylogger.info("loger created")
       return i,i+1
start_time = time.monotonic()

list1 = [i for i in range(1,10000)]
mylogger.info("thread started")
with ThreadPoolExecutor(max_workers=1000000,thread_name_prefix = "thread to add ") as executor:
   t = list(executor.map(test, list1))
mylogger.info("thread finished")
end_time = time.monotonic()
mylogger.info(timedelta(seconds=end_time - start_time))
# print(t)