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
