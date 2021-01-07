""" Endpoint URLs of the app """

from flask import flash, redirect, render_template, request, url_for

from flask_weather import app
from flask_weather.api import add_city, delete_city, get_weather


@app.route("/")
def home():
    """ Home Page """
    all_weather = get_weather()

    return render_template("result.html", all_weather=all_weather)


@app.route("/add", methods=["POST"])
def home_post():
    """ Add city to DB """
    err_msg = ""
    # Getting user input
    new_city = request.form.get("city").title()
    err_msg = add_city(new_city)
    if err_msg:
        flash(err_msg, "danger")
    else:
        flash("Successfull added new city!", "success")

    return redirect(url_for("home"))


@app.route("/delete/<city>")
def delete(city):
    """ Delete city from DB """
    city = delete_city(city)
    flash(f"Successfully deleted {city.name}", "success")

    return redirect(url_for("home"))
