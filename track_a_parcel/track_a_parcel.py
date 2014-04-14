#!/usr/bin/env python

from __future__ import print_function
import goslate
import urllib.request
import json
from collections import OrderedDict
import datetime
import hashlib
import sys

def log(mess):
    print("## LOG : ", mess, file=sys.stderr)

class Tracker():

    def __init__(self, dist_country="FR",
                 source_language="ru", target_language="en"):
        self.base_url = 'http://myparcels.ru/api/freeapp.php?cmd='
        self.API_KEY = "74ce6d236c8c53f64a7ed60d76bb3f94"
        self.DEVICE_ID = 354833057607398
        self.gs = goslate.Goslate()
        self.dist_country = dist_country.upper()
        self.source_language = source_language
        self.target_language = target_language

    def track_dict(self, track_nb):
        d = OrderedDict([("trackingNumber", None),
                        ("dstCountry", self.dist_country),
                        ("postalService", 'upu')])
        d["trackingNumber"] = track_nb
        return d

    def create_url_1(self, parcels):
        url = self.base_url
        url += "track&apiKey={api_key}&deviceId={device_id}&parcels={parcels}"
        return url.format(api_key=self.API_KEY,
                          device_id=self.DEVICE_ID,
                          parcels=parcels)

    def create_url_2(self, uid):
        url = self.base_url
        url += "status&apiKey={api_key}&deviceId={device_id}&requestId={uid}"
        return url.format(api_key=self.API_KEY,
                          device_id=self.DEVICE_ID,
                          uid=uid)

    def get_answer(self, url):
        return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

    def translate_date(self, _str):
        try:
            res = int(_str)
        except ValueError:
            return _str
        else:
            date = datetime.datetime.utcfromtimestamp(res)
            return date.strftime('%Y-%m-%d %H:%M:%S')

    def clean_html(self, _str):
        try:
            res = _str.split(', <span title=')[0]
        except:
            log('EXCEPTION : ', _str)
            res = _str
        else:
            return res

    def l10n(self, _str):
        """
        Localization fonction : translate from russian to english"""
        try:
            res = self.gs.translate(_str.encode("utf8"),
                                    target_language=self.target_language,
                                    source_language=self.source_language)
        except AssertionError:
            log("assertion error : ")
            log('    {}'.format(_str))
            res = _str
        except urllib.error.HTTPError as e:
            # error from google translate
            log(e, _str, sep='\n   ')
            res = _str
        return res.encode("utf8").decode("utf8")

    def interresting_field(self, answer):
        res = {"parcels": []}
        for parcel in answer["parcels"]:
            events = parcel["events"]
            events.sort(key=lambda x: x["date"])
            trackingNumber = parcel["trackingNumber"]
            l_events = []
            for event in events:
                res_event = {}
                res_event["country"] = event["country"]
                res_event["date"] = self.translate_date(event["date"])
                res_event["event"] = self.l10n(self.clean_html(event["event"]))
                res_event["eventId"] = event["eventId"]
                res_event['location'] = self.l10n(event["location"])
                l_events.append(res_event)

            tmp = {"events": l_events, "trackingNumber": trackingNumber}
            res["parcels"].append(tmp)
        return res

    def get_uid(self, answer):
        return answer['requestId']


    def get_track_info(self, l_track_nb):
        track = json.dumps([self.track_dict(nb) for nb in l_track_nb])
        url = self.create_url_1(track)
        answer = self.get_answer(url)
        uid = self.get_uid(answer)
        url = self.create_url_2(uid)
        answer = self.get_answer(url)
        return answer

    def track(self, l_tracking):
        answer = self.get_track_info(l_tracking)
        answer = self.interresting_field(answer)

        return answer


def get_md5(_object):
    return hashlib.md5(_object.__str__().encode("utf8")).hexdigest()


def load_parcels(fname):
    res = {}
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            l_elem = line.split(";")
            track_nb, seller, command, description = [e.strip() for e in l_elem]
            res[track_nb] = (description, command, seller)
        return res
