from flask import render_template, request

from app import app
from app.database.models import db, Parcels, ParcelEvents
from app.database.db_utils import get_or_create

from app.utils import async_update_events


@app.route('/')
def index():
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
