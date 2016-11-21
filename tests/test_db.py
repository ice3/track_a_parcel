"""Tests the database."""

import datetime

import pytest

from app import create_app
from app.database.models import Parcels, ParcelEvents
from app.database.models import db as _db
from app.database.db_utils import get_or_create


@pytest.yield_fixture(scope='function')
def app():
    """Create an app each for each test function."""
    app = create_app("testing_config")
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield app

    # app teardown here
    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(app):
    """Create a new database for each test function."""
    # NOTE: app, is required to keep the db in the right Flask app context
    _db.app = app
    _db.create_all()
    yield _db

    _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(app, db):
    """Create a new session for each test function."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    yield session

    # Finalize test here
    transaction.rollback()
    connection.close()
    session.remove()


def test_create_parcel(db):
    """Test that we can add an empty parcel."""
    p = Parcels(tracking_number="1")
    db.session.add(p)
    db.session.commit()
    assert p == db.session.query(Parcels).first()
    assert p.events == []


def test_db_reset(db):
    """Test that the database is correctly reset after each function."""
    p = Parcels(tracking_number="2")
    db.session.add(p)
    db.session.commit()
    assert 1 == len(db.session.query(Parcels).all())


def test_update_events(db):
    """Modify the events from a parcel."""
    p = Parcels(tracking_number="1")
    e1 = ParcelEvents()
    e2 = ParcelEvents()
    p.events = [e1, e2]
    db.session.add(p)
    db.session.commit()
    assert [e1, e2] == db.session.query(Parcels).first().events

    e3 = ParcelEvents()
    e4 = ParcelEvents()
    p.events = [e3, e4]
    db.session.add(p)
    db.session.commit()
    assert [e3, e4] == db.session.query(Parcels).first().events


def test_update_events_from_dict(db):
    """Update the events using a dictionnary."""
    event_dict = {
        'events': [{
            'country': '',
            'date': 1479505311,
            'event': 'Посылка добавлена на сайт',
            'eventId': '10',
            'location': '',
            'postalService': None,
            'weight': '0.000'
        }],
        'trackingNumber': 'RS806620392CN'}

    p = get_or_create(Parcels, tracking_number=event_dict["trackingNumber"])
    p.events = [ParcelEvents(), ParcelEvents()]
    db.session.commit()

    now = datetime.datetime.now()

    p.update_events(event_dict["events"])
    db.session.commit()

    assert event_dict["trackingNumber"] == p.tracking_number
    assert 1 == len(p.events)
    assert 'Посылка добавлена на сайт' == p.events[0].event
    assert now < p.updated


def test_get_or_create(db):
    """If an item already exist, get it otherwise create it."""
    number = "1"
    p1 = get_or_create(Parcels, tracking_number=number)
    db.session.commit()
    p2 = get_or_create(Parcels, tracking_number=number)
    db.session.commit()
    p3 = get_or_create(Parcels, tracking_number="2")
    db.session.commit()
    assert p1 == p2
    assert p3 != p1


def test_tracking_numbers_from_parcels(db):
    """Test the retreival of tracking numbers from the Parcels table."""
    assert [] == list(Parcels.tracking_numbers())

    db.session.add(Parcels(tracking_number="1"))
    db.session.add(Parcels(tracking_number="2"))
    db.session.commit()
    assert ["1", "2"] == list(Parcels.tracking_numbers())
