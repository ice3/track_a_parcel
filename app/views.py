import logging
from flask import render_template, request, jsonify

from app import app
from app.database.models import db, Parcels, ParcelEvents
from app.database.db_utils import get_or_create

logger = logging.getLogger('root')


@app.route('/')
def index():
    """Site root."""
    # async_update_events()
    parcels = db.session.query(Parcels).all()

    return render_template(
        "index.html",
        parcels=parcels
    )


@app.route("/api/parcel/", methods=['POST'])
def add_parcel():
    """Add or update a parcel to the database from the POST info."""
    tracking_number = request.form['tracking_number']
    description = request.form['description']

    p, created = get_or_create(Parcels, tracking_number=tracking_number)
    p.description = description
    db.session.add(p)
    db.session.commit()

    context = {
        "added": created,
        "html": render_template('parcel.html', parcel=p),
        "number": p.tracking_number,
    }

    return jsonify(context)


@app.route("/api/parcel/<string:tracking_number>", methods=['DELETE'])
def delete_parcel(tracking_number):
    """Delete a parcel from the database."""
    Parcels.query.filter_by(tracking_number=tracking_number).delete()
    db.session.commit()
    logger.info("deleted {}".format(tracking_number))

    return "removed {}".format(tracking_number)


@app.route("/api/parcel/<string:tracking_number>", methods=['UPDATE'])
def update_parcel(tracking_number):
    """Delete a parcel from the database."""
    p, created = get_or_create(Parcels, tracking_number=tracking_number)
    if 'toggle_received' in request.form:
        p.received = not p.received
        logger.info("toggled received for {}".format(tracking_number))

    db.session.add(p)
    db.session.commit()
    return jsonify({'received': p.received})


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


def city_format(city):
    try:
        return app.config['CITY_TRADS'][city]
    except KeyError as e:
        logger.exception(e)
        return city
