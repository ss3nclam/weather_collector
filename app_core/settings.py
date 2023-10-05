import logging
from configparser import ConfigParser


config = ConfigParser()
config.read('config.conf')
config = config


file_log = logging.FileHandler('Log.log')
console_out = logging.StreamHandler()
app_verbose = logging.basicConfig(
    handlers=(file_log, console_out),
    encoding = 'utf-8',
    format = '%(asctime)s %(levelname)s %(message)s',
    level = eval('logging.{}'.format('NOTSET'))
    )
