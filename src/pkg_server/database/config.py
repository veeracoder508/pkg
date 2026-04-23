from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


db = SQLAlchemy()

class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///my_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Base(DeclarativeBase): ...
