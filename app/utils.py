from app import app
from app.decorators import async
from app.tracker import Tracker
from app.database.models import db, Parcels
from app.database.db_utils import get_or_create


@async
def async_update_events():
    """Call update_events_from_api within a Thread."""
    with app.app_context():
        update_events_from_api()


def update_events_from_api():
    """Use the Tracking API to update events for registered parcels."""
    parcels_numbers = Parcels.tracking_numbers()
    tracker = Tracker()
    parcel_events = tracker.track(parcels_numbers)
    events_dicts = parcel_events['parcels']

    for events_dict in events_dicts:
        p = get_or_create(Parcels, tracking_number=events_dict['trackingNumber'])
        p.update_events(events_dict['events'])
        db.session.add(p)
