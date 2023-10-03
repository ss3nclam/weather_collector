import logging
import os
from configparser import ConfigParser
from datetime import date


config = ConfigParser()
config.read('config.conf')
config = config


writing_logs_stat = config['APP']['logs_to_file']

if writing_logs_stat == 'true':
    logging.info('Checking a logs\' folder..')
    try:
        os.mkdir('logs')
        logging.info('It was created!')
    except OSError:
        logging.info('It\'s already created.')


app_verbose = logging.basicConfig(
    filename = f'logs/{date.today()}.log' if writing_logs_stat == 'true' else None,
    encoding = 'utf-8',
    format = '%(asctime)s %(levelname)s %(message)s',
    level = eval('logging.{}'.format('NOTSET'))
    )