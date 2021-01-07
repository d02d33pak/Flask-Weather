""" API functions to interact with Model (db) """

import os

import requests

from flask_weather import db
from flask_weather.models import City


def add_city(new_city):
    """ Adds new city in db """
    resp = ""
    if new_city:
        # Checking if city aleady exist in DB
        city_exist = City.query.filter_by(name=new_city).first()
        if not city_exist:
            city_data = get_city_weather(new_city)
            # Fetching and checking if city is valid
            if city_data["cod"] == 200:
                city_obj = City(name=city_data["name"])
                db.session.add(city_obj)
                db.session.commit()
            else:
                resp = "Invalid City!"
        else:
            resp = "City Already Exist!"

    return resp


def delete_city(city_name):
    """ Deletes city from db """
    city = City.query.filter_by(name=city_name).first()
    db.session.delete(city)
    db.session.commit()

    return city


def get_weather():
    """ Fetches weather for all cities in db """
    all_weather = list()
    cities = City.query.order_by(City.id.desc()).all()

    for city in cities:
        response = get_city_weather(city.name)
        weather = {
            "city": response["name"],
            "temp": response["main"]["temp"],
            "desc": response["weather"][0]["description"].title(),
            "icon": response["weather"][0]["icon"],
        }
        all_weather.append(weather)

    return all_weather


def get_city_weather(city):
    """ Returns weather data for specific city """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "units": "metric",
        "appid": os.getenv("API_KEY"),
    }

    return requests.get(url, params=params).json()
