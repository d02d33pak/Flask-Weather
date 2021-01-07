""" Initialization of app and db """

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setting up Flask
app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
# Setting up sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///..///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# to avoid circular import
from flask_weather import views
