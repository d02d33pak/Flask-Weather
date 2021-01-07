""" Database models for the app """

from flask_weather import db


class City(db.Model):
    """ Model Class to hold City data """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
