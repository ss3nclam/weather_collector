import time
import logging

import schedule

from app_core.data import (check_cities_table, commit_weather, get_cities_list,
                           get_weather, init_cities, validate_db)
from app_core.settings import app_verbose, config


def job(cities):
    for city in cities:
        weather = get_weather(city['name'], city['longitude'], city['latitude'])
        if weather:
            commit_weather(city['name'], weather)


def main():
    validate_db()
    cities_list = get_cities_list()
    if cities_list:
        time_delta = int(config['APP']['scheduler_time_delta'])
        schedule.every(time_delta).hours.do(job, cities_list)
        # schedule.every(15).seconds.do(job, cities_list)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        logging.error('Something was wrong!')


if __name__ == '__main__':
    main()