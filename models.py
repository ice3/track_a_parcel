"""Database models using sqlalchemy.

The models are :
 * Parcels with the parcel information
 * ParcelEvents with the events related to a parcel
"""

import datetime

from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class Parcels(Base):
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

    def update_events(self, events):
        """Update the list of events with the one provided as argument."""
        self.events = []
        for event in events:
            e = ParcelEvents.from_api_dict(event)
            self.events.append(e)
        self.updated = datetime.datetime.now()

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


class ParcelEvents(Base):
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


def get_or_create(session, model, **kwargs):
    """Get a row if exist otherwise create it.

    Copy of django orm get_or_create.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

engine = create_engine('sqlite:///tmp.db')
Base.metadata.create_all(engine)



def main():
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///:memory:', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    p = Parcels(tracking_number="2")
    session.add(p)

    e1 = ParcelEvents(
        location="FR",
        event="Arrivé",
        event_id=1,
        date=datetime.datetime.today()
    )
    e2 = ParcelEvents(
        location="Lille",
        event="Départ",
        event_id=2,
        date=datetime.datetime.today() - datetime.timedelta(1)
    )
    p.events = [e1, e2]
    p.updated = datetime.datetime.now()
    session.add(p)
    session.commit()

    e3 = ParcelEvents(
        location="FR",
        event="Arrivé",
        event_id=3,
        date=datetime.datetime.today() - datetime.timedelta(2)
    )
    e4 = ParcelEvents(
        location="Lille",
        event="Départ",
        event_id=4,
        date=datetime.datetime.today() - datetime.timedelta(3)
    )
    p.events = [e3, e4]
    p.updated = datetime.datetime.now()
    session.add(p)
    session.commit()

    p = session.query(Parcels).first()
    print(p)
    print("  * " + "\n  * ".join([str(e) for e in p.events]))


if __name__ == '__main__':
    main()