"""Init file for the track_a_parcel app."""

from flask import Flask
from app.database.models import db


def create_app(config):
    """App factory to specify the configuratin object."""
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app('config')

from app import views
app.jinja_env.filters['datetimeformat'] = views.datetimeformat
app.jinja_env.filters['event_format'] = views.event_format

from app.database import models
