import time
import logging

from app import app
from app.decorators import async
from app.tracker.tracker import Tracker
from app.database.models import db, Parcels
from app.database.db_utils import get_or_create


logger = logging.getLogger('root')


@async
def apply_periodically(f, period):
    """Apply a function in background each period seconds.

    Input :
        f : a function
        period : the apply interval in seconds
    """
    with app.app_context():
        last_applied = time.time()
        f()

        while True:
            time.sleep(1)
            if (time.time() - last_applied) > period:
                last_applied = time.time()
                f()
                logger.debug("applied function {} periodically".format(f.__name__))


def update_events_periodically(period):
    """Update the events in database each period seconds."""
    apply_periodically(update_events_from_api, period)


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
    if not parcel_events:
        return
    events_dicts = parcel_events['parcels']

    for events_dict in events_dicts:
        p = get_or_create(Parcels, tracking_number=events_dict['trackingNumber'])
        p.update_events(events_dict['events'])
        db.session.add(p)
