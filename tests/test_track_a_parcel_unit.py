#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_track_a_parcel
----------------------------------

Tests for `track_a_parcel` module.
"""

import pytest
from track_a_parcel.track_a_parcel import Tracker

from collections import OrderedDict
import json

@pytest.fixture
def tracker_simple():
    return Tracker()

@pytest.fixture
def tracker_custom():
    return Tracker("MC", "en", "fr")


@pytest.fixture
def tracker_no_l10n():
    # we don't want to have call to google translate in unit tests
    t = Tracker()
    t.l10n = lambda x:  x
    return t


def test_dist_country(tracker_simple):
    tracker = tracker_simple
    assert tracker.dist_country == "FR"


def test_source_lang(tracker_simple):
    tracker = tracker_simple
    assert tracker.source_language == "ru"


def test_taget_lang(tracker_simple):
    tracker = tracker_simple
    assert tracker.target_language == "en"


def test_base_url(tracker_simple):
    tracker = tracker_simple
    assert tracker.base_url == 'http://myparcels.ru/api/freeapp.php?cmd='


def test_dest_country_custom(tracker_custom):
    tracker = tracker_custom
    assert tracker.dist_country == "MC"


def test_source_lang_custom(tracker_custom):
    tracker = tracker_custom
    assert tracker.source_language == "en"


def test_taget_lang_custom(tracker_custom):
    tracker = tracker_custom
    assert tracker.target_language == "fr"


def test_base_url_custom(tracker_custom):
    tracker = tracker_custom
    assert tracker.base_url == 'http://myparcels.ru/api/freeapp.php?cmd='

def test_track_dict(tracker_simple):
    tracker = tracker_simple
    track_number = "123456789"
    t_res = tracker.track_dict(track_number)
    res = OrderedDict([("trackingNumber", track_number),
                      ("dstCountry", "FR"),
                      ("postalService", 'upu')])
    assert t_res == res


def test_url_1(tracker_simple):
    parcel = ('{"trackingNumber": 123456789, '
              '"dstCountry": "FR", "postalService": "upu"}')

    res = ('http://myparcels.ru/api/freeapp.php?cmd=track&apiKey='
           '74ce6d236c8c53f64a7ed60d76bb3f94&deviceId=354833057607398'
           '&parcels={"trackingNumber": 123456789, "dstCountry"'
           ': "FR", "postalService": "upu"}')

    assert res == tracker_simple.create_url_1(parcel)

def test_url_1_multiple_items(tracker_simple):

    parcels = ('[{"trackingNumber": "123456789", '
               '"dstCountry": "FR", "postalService": "upu"}, '
               '{"trackingNumber": "987654321", '
               '"dstCountry": "FR", "postalService": "upu"}]')
    res = ('http://myparcels.ru/api/freeapp.php?cmd=track&apiKey='
           '74ce6d236c8c53f64a7ed60d76bb3f94&deviceId=354833057607398'
           '&parcels=[{"trackingNumber": "123456789", "dstCountry": "FR", '
           '"postalService": "upu"}, {"trackingNumber": "987654321", '
           '"dstCountry": "FR", "postalService": "upu"}]')

    assert res == tracker_simple.create_url_1(parcels)


def test_answer_1(tracker_simple):
    answer = {"requestId": 1845381, "timeout": 26}
    assert 1845381 == tracker_simple.get_uid(answer)


def test_url_2(tracker_simple):
    uid = "12345"
    res = ('http://myparcels.ru/api/freeapp.php?cmd=status&apiKey='
           '74ce6d236c8c53f64a7ed60d76bb3f94&deviceId=354833057607398'
           '&requestId=12345')
    assert res == tracker_simple.create_url_2(uid)


def test_translate_date_ok(tracker_simple):
    ts = "1395998892"
    date = '2014-03-28 09:28:12'
    assert tracker_simple.translate_date(ts) == date


def test_translate_date_ko(tracker_simple):
    ts = "not_working"
    assert tracker_simple.translate_date(ts) == ts


def test_clean_html_ok(tracker_simple):
    text = 'something + other, <span title="details">other</span>'
    assert tracker_simple.clean_html(text) == 'something + other'


def test_clean_html_ko(tracker_simple):
    text = 'something  "details" | + other '
    assert tracker_simple.clean_html(text) == text


def test_clean_html_2(tracker_simple):
    text = 'something, something else, <span title="details">other</span>'
    assert tracker_simple.clean_html(text) == 'something, something else'


def test_l10n(tracker_custom):
    to_translate = 'hello'
    res = 'bonjour'
    assert res == tracker_custom.l10n(to_translate)


def test_interresting_field(tracker_no_l10n):
    a = \
    {
    'parcels': [{
        'trackingNumber': 'RC486713055CN',
        'events': [{
            'date': 1396411140,
            'postalService': 'Почта Китая',
            'event': 'Передана таможне, <span title="Guangzhou, 广州国际">Гуанчжоу</span>',
            'detailedLocation': 'Guangzhou, 广州国际',
            'weight': 0.000,
            'country': 'CN',
            'eventId': 125,
            'location': 'Гуанчжоу'
        }, {
            'date': 1397225788,
            'postalService': None,
            'event': 'Посылка добавлена на сайт',
            'detailedLocation': '',
            'weight': 0.000,
            'country': '',
            'eventId': 10,
            'location': ''
        }]
    }, {
        'trackingNumber': 'RC107023715CN',
        'events': [{
            'date': 1396676460,
            'postalService': 'Почта Китая',
            'event': 'Поступила на почту Китая, <span title="Jiangmen, 广东江门开平广告">Цзянмэнь</span>',
            'detailedLocation': 'Jiangmen, 广东江门开平广告',
            'weight': 0.000,
            'country': 'CN',
            'eventId': 110,
            'location': 'Цзянмэнь'
        }, {
            'date': 1397225788,
            'postalService': None,
            'event': 'Посылка добавлена на сайт',
            'detailedLocation': '',
            'weight': 0.000,
            'country': '',
            'eventId': 10,
            'location': ''
        }]
    }]
}

    res = \
{
    'parcels': [{
        'trackingNumber': 'RC486713055CN',
        'events': [{
            'location': 'Гуанчжоу',
            'date': '2014-04-02 03:59:00',
            'country': 'CN',
            'eventId': 125,
            'event': 'Передана таможне'
        }, {
            'location': '',
            'date': '2014-04-11 14:16:28',
            'country': '',
            'eventId': 10,
            'event': 'Посылка добавлена на сайт'
        }]
    }, {
        'trackingNumber': 'RC107023715CN',
        'events': [{
            'location': 'Цзянмэнь',
            'date': '2014-04-05 05:41:00',
            'country': 'CN',
            'eventId': 110,
            'event': 'Поступила на почту Китая'
        }, {
            'location': '',
            'date': '2014-04-11 14:16:28',
            'country': '',
            'eventId': 10,
            'event': 'Посылка добавлена на сайт'
        }]
    }]
}


    res_try = tracker_no_l10n.interresting_field(a)
    assert res == res_try
