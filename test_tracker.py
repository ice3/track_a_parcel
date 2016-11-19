"""Tests for the tracker file."""

import pytest

from tracker import Tracker

"""
Multiple parcels API result :


{'parcels': [{'events': [{'country': 'NL',
                          'date': 1475801880,
                          'detailedLocation': '',
                          'event': 'Информация о посылке поступила в '
                                   'электронном виде',
                          'eventId': '100',
                          'location': '',
                          'postalService': 'Почта Нидерландов',
                          'weight': '0.000'},
                         {'country': 'NL',
                          'date': 1475853480,
                          'detailedLocation': '',
                          'event': 'Прибыла в сортировочный центр',
                          'eventId': '160',
                          'location': '',
                          'postalService': 'Почта Нидерландов',
                          'weight': '0.000'},
                         {'country': 'NL',
                          'date': 1475856120,
                          'detailedLocation': '',
                          'event': 'Сортировка',
                          'eventId': '165',
                          'location': '',
                          'postalService': 'Почта Нидерландов',
                          'weight': '0.000'},
                         {'country': 'NL',
                          'date': 1475917440,
                          'detailedLocation': '',
                          'event': 'Покинула почту',
                          'eventId': '180',
                          'location': '',
                          'postalService': 'Почта Нидерландов',
                          'weight': '0.000'},
                         {'country': '',
                          'date': 1479505968,
                          'detailedLocation': '',
                          'event': 'Посылка добавлена на сайт',
                          'eventId': '10',
                          'location': '',
                          'postalService': None,
                          'weight': '0.000'}],
              'trackingNumber': 'RS619965431NL'},
             {'events': [{'country': '',
                          'date': 1479505311,
                          'detailedLocation': '',
                          'event': 'Посылка добавлена на сайт',
                          'eventId': '10',
                          'location': '',
                          'postalService': None,
                          'weight': '0.000'}],
              'trackingNumber': 'RS806620392CN'}]}



"""


@pytest.fixture
def my_tracker():
    return Tracker()


def test_simple_parcel_string(my_tracker):
    expected = '[{"trackingNumber": 1, "dstCountry": "FR", "postalService": "upu"}]'
    parcel_string = my_tracker.parcel_string(
        [[1]]
    )
    assert parcel_string == expected

def test_parcel_with_options_string(my_tracker):
    expected = '[{"trackingNumber": 1, "dstCountry": "DE", "postalService": "..."}]'
    parcel_string = my_tracker.parcel_string(
        [[1, "DE", "..."]]
    )
    assert parcel_string == expected

def test_multiple_parcels_string(my_tracker):
    expected = '[{"trackingNumber": 1, "dstCountry": "FR", "postalService": "upu"}, {"trackingNumber": 2, "dstCountry": "FR", "postalService": "upu"}]'
    parcels_string = my_tracker.parcel_string(
        [
            [1], [2]
        ]
    )

    assert parcels_string == expected

