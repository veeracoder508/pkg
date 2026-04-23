from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): ...

db = SQLAlchemy(model_class=Base)

class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///pkg_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
