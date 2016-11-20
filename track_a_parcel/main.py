from models import Parcels, ParcelEvents, get_or_create
from tracker import Tracker

import json

data = {
    'parcels':
        [{'events':
            [{
                'country': 'NL',
                'date': 1475801880,
                'detailedLocation': '',
                'event': 'Информация о посылке поступила в '
                'электронном виде',
                'eventId': '100',
                'location': '',
                'postalService': 'Почта Нидерландов',
                'weight': '0.000'
            }, {
                'country': 'NL',
                'date': 1475853480,
                'detailedLocation': '',
                'event': 'Прибыла в сортировочный центр',
                'eventId': '160',
                'location': '',
                'postalService': 'Почта Нидерландов',
                'weight': '0.000'
            }, {
                'country': 'NL',
                'date': 1475856120,
                'detailedLocation': '',
                'event': 'Сортировка',
                'eventId': '165',
                'location': '',
                'postalService': 'Почта Нидерландов',
                'weight': '0.000'
            }, {
                'country': 'NL',
                'date': 1475917440,
                'detailedLocation': '',
                'event': 'Покинула почту',
                'eventId': '180',
                'location': '',
                'postalService': 'Почта Нидерландов',
                'weight': '0.000'
            }, {
                'country': '',
                'date': 1479505968,
                'detailedLocation': '',
                'event': 'Посылка добавлена на сайт',
                'eventId': '10',
                'location': '',
                'postalService': None,
                'weight': '0.000'
            }],
            'trackingNumber': 'RS619965431NL'
        }, {
        'events':
            [{
                'country': '',
                'date': 1479505311,
                'event': 'Посылка добавлена на сайт',
                'eventId': '10',
                'location': '',
                'postalService': None,
                'weight': '0.000'
            }],
            'trackingNumber': 'RS806620392CN'}]
}


def main():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine('sqlite:///tmp.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    for parcel in data["parcels"]:
        events = parcel["events"]
        number = parcel["trackingNumber"]
        p = get_or_create(Parcels, tracking_number=number)
        p.update_events(events)
        db.session.add(p)
        db.session.commit()

    import IPython; IPython.embed()

if __name__ == '__main__':
    main()