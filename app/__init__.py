"""Init file for the track_a_parcel app.

"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import db


def create_app(config):
    """App factory to specify the configuratin object."""
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    return app, db

app, db = create_app('config')

from app import models