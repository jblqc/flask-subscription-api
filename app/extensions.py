from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate

"""
    This file contains the extensions for the API, the database and the api.
    """
api = Api()
db = SQLAlchemy()
migrate = Migrate()


