from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): """"""

db = SQLAlchemy(model_class=Base)

class Config(object):
    """The config object for the database.
    
    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The URI for the database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Whether to track database modifications.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///pkg_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
