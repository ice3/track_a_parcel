"""Database models using sqlalchemy.

The models are :
 * Parcels with the parcel information
 * ParcelEvents with the events related to a parcel
"""

import datetime
import logging

from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

logger = logging.getLogger('root')


class Parcels(db.Model):
    """A database table containing the parcel information.

    A parcel is descrived with :
     * a unique tracking_number
     * a destination_country, defaults to France
     * a postal_service, defaults to upu
     * the add in database date
     * the date of last update
     * a list of events (foreign keys to ParcelEvents)
    """

    __tablename__ = 'parcels'

    tracking_number = Column(String, primary_key=True)
    destination_country = Column(String, default="FR")
    postal_service = Column(String, default="upu")
    added = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, onupdate=datetime.datetime.now)
    description = Column(String)
    received = Column(Boolean, default=False)

    events = relationship(
        "ParcelEvents",
        back_populates="parcel",
    )

    def update_events(self, dict_events):
        """Update the list of events with the one provided as argument."""
        events = []
        for dict_event in dict_events:
            e = ParcelEvents.from_api_dict(dict_event)
            events.append(e)

        logger.debug(
            ("already present events number: {} "
             "-- new events number: {}").format(len(self.events), len(events)))

        if len(events) > len(self.events):
            logger.info("updating events for {}".format(self))
            self.events = events
            self.updated = datetime.datetime.now()
        else:
            logger.info("not updating events for {}".format(self))
        logger.info("{}".format(self))
        db.session.commit()

    def last_updated(self):
        """If the parcel has never been updated, we return the creation date."""
        return self.updated or self.added

    @classmethod
    def active_tracking_numbers(cls):
        """Return all the active tracking_numbers (the ones not received).

        When the database grow, I wonder if we should paginate here or where we use the data...
        """
        return db.session\
            .query(cls.tracking_number)\
            .filter_by(received=False)\
            .all()

    @classmethod
    def all_tracking_numbers(cls):
        """Return all the active tracking_numbers (the ones not received).

        When the database grow, I wonder if we should paginate here or where we use the data...
        """
        return db.session\
            .query(cls.tracking_number)\
            .all()

    def __repr__(self):
        return ("<Parcel(tracking_number = {} -- "
                "destination = {} -- postal_service = {} -- "
                "added = {} -- last update = {} -- {} events)").format(
                    self.tracking_number,
                    self.destination_country,
                    self.postal_service,
                    self.added,
                    self.updated,
                    len(self.events)
        )


class ParcelEvents(db.Model):
    """A database table containing the parcel events.

    These events are related to a parcel.

    The rows also contain original and translated versions of the postal service and event messages.
    """

    __tablename__ = "parcel_events"

    id = Column(Integer, primary_key=True)
    parcel_number = Column(String, ForeignKey('parcels.tracking_number'))
    parcel = relationship("Parcels", back_populates="events")

    date = Column(DateTime)
    event = Column(String)
    event_id = Column(Integer)
    location = Column(String)
    postal_service = Column(String)
    weight = Column(Float)

    postal_service_translated = Column(String)
    event_translated = Column(String)

    @classmethod
    def from_api_dict(cls, api_dict):
        """Create an event from the API response."""
        obj = cls()
        obj.date = datetime.datetime.fromtimestamp(api_dict["date"])
        obj.event = api_dict["event"]
        obj.event_id = api_dict["eventId"]
        obj.location = api_dict["location"]
        obj.postal_service = api_dict["postalService"]
        obj.weight = api_dict["weight"]
        return obj

    def __repr__(self):
        return ("<TrackingEvent(parcel = {} -- "
                "date = {} -- postal_service = {} -- "
                "event = {} -- event_id = {} -- weight = {} -- location = {})").format(
                    self.parcel_number,
                    self.date,
                    self.postal_service,
                    self.event,
                    self.event_id,
                    self.weight,
                    self.location,
        )
