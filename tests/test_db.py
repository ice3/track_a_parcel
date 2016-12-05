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


def test_no_event_update_when_smaller_number_of_events(db):
    """We do not update when we lose some events."""
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

    p, created = get_or_create(Parcels, tracking_number=event_dict["trackingNumber"])
    p.events = [ParcelEvents(), ParcelEvents()]
    p.updated = datetime.datetime.now()
    db.session.commit()

    now = datetime.datetime.now()

    p.update_events(event_dict["events"])
    db.session.commit()

    assert event_dict["trackingNumber"] == p.tracking_number
    assert 2 == len(p.events)
    assert now > p.updated


def test_events_update_when_more_events(db):
    """We assume that we can only get more events as time pass.

    We don't touch the database if we get less or the same number of events.
    """
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

    p, created = get_or_create(Parcels, tracking_number=event_dict["trackingNumber"])
    p.updated = datetime.datetime.now()
    db.session.commit()

    now = datetime.datetime.now()

    p.update_events(event_dict["events"])
    db.session.commit()

    assert event_dict["trackingNumber"] == p.tracking_number
    assert 1 == len(p.events)
    assert "Посылка добавлена на сайт" in p.events[0].event
    assert now < p.updated


def test_get_or_create(db):
    """If an item already exist, get it otherwise create it."""
    number = "1"
    p1, created1 = get_or_create(Parcels, tracking_number=number)
    db.session.commit()
    p2, created2 = get_or_create(Parcels, tracking_number=number)
    db.session.commit()
    p3, created3 = get_or_create(Parcels, tracking_number="2")
    db.session.commit()
    assert p1 == p2
    assert p3 != p1
    assert created1 is True
    assert created3 is True
    assert created2 is False


def test_tracking_numbers_from_parcels(db):
    """Test the retreival of tracking numbers from the Parcels table."""
    assert [] == list(Parcels.all_tracking_numbers())

    db.session.add(Parcels(tracking_number="1"))
    db.session.add(Parcels(tracking_number="2"))
    db.session.commit()
    assert [("1",), ("2",)] == list(Parcels.all_tracking_numbers())


def test_received_parcels(db):
    """Test that we don't list the already received parcels."""
    assert [] == list(Parcels.active_tracking_numbers())

    p1 = Parcels(tracking_number="1")
    p2 = Parcels(tracking_number="2", received=True)

    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

    actives = Parcels.active_tracking_numbers()
    assert 1 == len(actives)
    assert (p1.tracking_number,) in actives
    assert (p2.tracking_number,) not in actives
