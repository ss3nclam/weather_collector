from datetime import datetime

import requests
from sqlalchemy import select

from app_core.db_engine import session
from app_core.db_models import City, Weather
from app_core.settings import config


def check_cities_table():
    db_req = select(City)
    try:
        cities_list = list(session.scalars(db_req))
        return True if len(cities_list) == 50 else False
    except Exception:
        return


def init_cities():
    link = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-500/records?order_by=population%20desc&limit=50'
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
        print('The list of cities was successfully created!')
    except Exception as error:
        print(f'[ERROR] - {error}')


def get_cities_list():
    print('Getting the list of cities..')
    try:
        cities = []
        for row in session.execute(select(City)):
            city = {'id':row.City.id, 'name':row.City.name, 'longitude':row.City.longitude, 'latitude':row.City.latitude}
            cities.append(city)
        print('Successfully!')
        return cities
    except Exception as error:
        print(f'[ERROR] - {error}')
        return


def get_weather(id, name, longitude, latitude):
    print(f'Getting the weather for [id={id}, name={name}]..')
    req_param = {
    'appid':config['OPEN_WEATHER_API']['appid'],
    'units':config['OPEN_WEATHER_API']['units'],
    'lat':latitude,
    'lon':longitude
    }
    try:
        request = requests.get("http://api.openweathermap.org/data/2.5/weather", params=req_param)
        print('Successfully!')
        return request.json().get('main')
    except Exception as error:
        print(f'[ERROR] - {error}')
        return


def commit_weather(city_id, weather_info):
    print('Commiting..')
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
        print('Done!')
    except Exception as error:
        print(f'[ERROR] - {error}')
