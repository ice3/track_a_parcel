from flask import render_template

from app import app
from app.database.models import db, Parcels, ParcelEvents

@app.route('/')
@app.route('/index')
def index():
    print()
    return render_template(
        "index.html",
        parcels=db.session.query().all()
    )
