"""Database models using sqlalchemy.

The models are :
 * Parcels with the parcel information
 * ParcelEvents with the events related to a parcel
"""

import datetime


from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    events = relationship(
        "ParcelEvents",
        back_populates="parcel",
    )

    def update_events(self, dict_events):
        """Update the list of events with the one provided as argument."""
        self.events = []
        for dict_event in dict_events:
            e = ParcelEvents.from_api_dict(dict_event)
            self.events.append(e)
        self.updated = datetime.datetime.now()

    @classmethod
    def tracking_numbers(cls):
        return (e[0] for e in db.session.query(cls.tracking_number).all())

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
                "event = {} -- event_id = {} -- weight = {})").format(
                    self.parcel_number,
                    self.date,
                    self.postal_service,
                    self.event,
                    self.event_id,
                    self.weight,
        )
