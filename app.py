"""
Flask Weather App

Author: Deepak Talan
Github: @d02d33pak
"""

import os

import requests
from flask import Flask, flash, redirect, render_template, request, url_for

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class City(db.Model):
    """ Model Class to hold City data """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_city_weather(city):
    """ Returns weather data for specific city """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "units": "metric",
        "appid": os.getenv("API_KEY"),
    }
    return requests.get(url, params=params).json()


@app.route("/")
def home():
    """ Home Page """
    all_weather = []
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
    return render_template("result.html", all_weather=all_weather)


@app.route("/add", methods=["POST"])
def home_post():
    """ Add city to DB """
    err_msg = ""
    new_city = request.form.get("city").title()
    if new_city:
        city_exist = City.query.filter_by(name=new_city).first()
        if not city_exist:
            city_data = get_city_weather(new_city)
            print(city_data["cod"])
            if city_data["cod"] == 200:
                city_obj = City(name=city_data["name"])
                db.session.add(city_obj)
                db.session.commit()
            else:
                err_msg = "Invalid City!"
        else:
            err_msg = "City Already Exist!"
    if err_msg:
        flash(err_msg, "danger")
    else:
        flash("Successfull added new city!", "success")
    return redirect(url_for("home"))


@app.route("/delete/<city>")
def delete(city):
    """ Delete city from DB """
    city = City.query.filter_by(name=city).first()
    db.session.delete(city)
    db.session.commit()
    flash(f"Successfully deleted {city.name}", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
