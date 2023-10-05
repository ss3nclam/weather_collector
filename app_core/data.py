import logging
import time
from datetime import datetime

import requests
from sqlalchemy import inspect, select

from app_core.db_engine import engine, session
from app_core.db_models import City, Weather, create_tables
from app_core.settings import config


def check_cities_table():
    logging.info('Checking the list of cities..')
    db_req = select(City)
    try:
        cities_list = list(session.scalars(db_req))
        if cities_list:
            logging.info('The list of cities has been discovered!')
            return True
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


def validate_db():
    db_name = config['DATABASE']['db_name']
    logging.info('Checking db connection..')
    try:
        connection = engine.connect()
        logging.info('Connection established!')
    except Exception as error:
        logging.error(error)
        logging.info('Waiting db connection (15 sec)..')
        time.sleep(15)
        validate_db()
    else:
        logging.info('Checking tables..')
        inspector = inspect(engine)
        if inspector.has_table('cities', db_name) and inspector.has_table('weather', db_name):
            logging.info('OK')
        else:
            create_tables()
        if not check_cities_table():
            init_cities()


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


def get_weather(name, longitude, latitude):
    logging.info(f'Getting the weather for name={name}..')
    req_param = {
    'appid':config['OPEN_WEATHER_API']['appid'],
    'units':'metric',
    'lat':latitude,
    'lon':longitude
    }
    try:
        request = requests.get("http://api.openweathermap.org/data/2.5/weather", params=req_param)
        logging.info('Successfully gotten!')
        return request.json()
    except Exception as error:
        logging.error(f'Can\'t get the weather for name={name} - {error}')
        return


def commit_weather(name, weather_info):
    logging.info(f'Commiting weather info for city name={name}..')
    w_main = weather_info.get('main')
    w_wind = weather_info.get('wind')
    try:
        weather = Weather(
            city=name,
            temp=w_main['temp'],
            temp_min=w_main['temp_min'],
            temp_max=w_main['temp_max'],
            wind_speed=w_wind['speed'],
            wind_deg=w_wind['deg'],
            pressure=w_main['pressure'],
            humidity=w_main['humidity'],
            added_at=datetime.now()
            )
        session.add(weather)
        session.commit()
        logging.info('Successfully!')
    except Exception as error:
        logging.error(f'Can\'t commit the weather for name={name} - {error}')
