import logging
from datetime import datetime

import requests
from sqlalchemy import select, delete

from app_core.db_engine import session
from app_core.db_models import City, Weather
from app_core.settings import config


def check_cities_table():
    logging.info('Checking the list of cities..')
    db_req = select(City)
    try:
        cities_list = list(session.scalars(db_req))
        if cities_list:
            logging.info('The list of cities has been discovered!')
            return True

            # if len(cities_list) == config['APP']['cities_limit']:
            #     logging.info('The list of cities has been discovered!')
            #     return True
            # else:
            #     logging.critical('Need to rewrite cities table!')
            #     logging.info('The cities\' list rewriting..')
            #     try:
            #         session.execute(delete(City))
            #         logging.nfo('Successfully rewrited!')
            #         return False
            #     except Exception as error:
            #         logging.error(error)
            #         return
        else:
            logging.info('The list of cities has not been discovered.')
            return False
    except Exception as error:
        logging.error(error)
        return


def init_cities():
    logging.info('Creating the list of cities..')
    cities_limit = config['APP']['cities_limit']
    link = f'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-500/records?order_by=population%20desc&limit={cities_limit}'
    try:
        req = requests.get(link)
        cities_list = [
            {'name':city['name'],
             'longitude':city['coordinates']['lon'],
             'latitude':city['coordinates']['lat'],
             'timezone':city['timezone']
             } for city in req.json().get('results')
            ]
        
        for city in cities_list:
            with session:
                new_city = City(name=city['name'], longitude=city['longitude'], latitude=city['latitude'], timezone=city['timezone'])
                session.add(new_city)
                session.commit()
        logging.info('The list of cities was successfully created!')
    except Exception as error:
        logging.error(error)


def get_cities_list():
    logging.info('Getting the list of cities..')
    try:
        cities = []
        for row in session.execute(select(City)):
            city = {'id':row.City.id, 'name':row.City.name, 'longitude':row.City.longitude, 'latitude':row.City.latitude}
            cities.append(city)
        logging.info('The list of cities was successfully gotten!')
        return cities
    except Exception as error:
        logging.error(error)
        return


def get_weather(id, name, longitude, latitude):
    logging.info(f'Getting the weather for [id={id}, name={name}]..')
    req_param = {
    'appid':config['OPEN_WEATHER_API']['appid'],
    'units':config['OPEN_WEATHER_API']['units'],
    'lat':latitude,
    'lon':longitude
    }
    try:
        request = requests.get("http://api.openweathermap.org/data/2.5/weather", params=req_param)
        logging.info('Successfully gotten!')
        return request.json().get('main')
    except Exception as error:
        logging.error(f'Can\'t get the weather for [id={id}, name={name}] - {error}')
        return


def commit_weather(city_id, name, weather_info):
    logging.info(f'Commiting weather info for city [id={city_id}, name={name}]..')
    try:
        weather = Weather(
            city_id=city_id,
            temp=weather_info['temp'],
            temp_min=weather_info['temp_min'],
            temp_max=weather_info['temp_max'],
            added_at=datetime.now()
            )
        session.add(weather)
        session.commit()
        logging.info('Successfully!')
    except Exception as error:
        logging.error(f'Can\'t commit the weather for [id={city_id}, name={name}] - {error}')
