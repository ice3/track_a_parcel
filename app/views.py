import logging
from flask import render_template, request

from app import app
from app.database.models import db, Parcels, ParcelEvents
from app.database.db_utils import get_or_create

from app.utils import async_update_events

logger = logging.getLogger('root')


@app.route('/')
def index():
    """Site root."""
    async_update_events()
    parcels = db.session.query(Parcels).all()

    return render_template(
        "index.html",
        parcels=parcels
    )


@app.route("/add", methods=["POST"])
def add_parcel():
    """Add a new parcel to the database from the POST info."""
    tracking_number = request.form.tracking_number
    description = request.form.description

    p = get_or_create(Parcels, tracking_number=tracking_number)
    p.description = description
    db.session.add(p)
    db.session.commit()


def datetimeformat(value, format='%d-%m-%Y'):
    """Format date time object."""
    return value.strftime(format)


def event_format(event_id):
    """Try to translate an event from its event id."""
    try:
        return app.config['EVENT_TRADS'][event_id]
    except KeyError as e:
        logger.exception(e)
        return event_id
