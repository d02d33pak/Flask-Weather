"""
Flask Weather App

Author: Deepak Talan
Github: @d02d33pak
"""

from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "72d88c977f3005dddf57beeda2469564"
URL = "api.openweathermap.org/data/2.5/weather?q={city name}&appid={your api key}"


@app.route("/")
def home():

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
