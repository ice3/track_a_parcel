#!/usr/bin/env python

import goslate
import urllib.request
import json
from pprint import pprint
from collections import OrderedDict
import datetime
import hashlib

base_url = 'http://myparcels.ru/api/freeapp.php?cmd='
API_KEY = "74ce6d236c8c53f64a7ed60d76bb3f94"
DEVICE_ID = 354833057607398
gs = goslate.Goslate()


def track_dict(track_nb):
    d = OrderedDict([("trackingNumber", None),
                 ("dstCountry", 'FR'),
                 ("postalService", 'upu')])
    d["trackingNumber"] = track_nb
    return d

def create_url_1(parcels):
    init_url = base_url
    init_url += "track&apiKey={api_key}&deviceId={device_id}&parcels={parcels}"
    return init_url.format(api_key=API_KEY,
                           device_id=DEVICE_ID,
                           parcels=parcels)

def create_url_2(uid):
    ans_url = base_url
    ans_url += "status&apiKey={api_key}&deviceId={device_id}&requestId={uid}"
    return ans_url.format(api_key=API_KEY, device_id=DEVICE_ID, uid=uid)


def get_answer(url):
    return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))


def translate_date(_str):
    try:
        res = int(_str)
    except ValueError:
        return _str
    else:
        date = datetime.datetime.fromtimestamp(res)
        return date.strftime('%Y-%m-%d %H:%M:%S')


def clean_html(_str):
    try:
        res = _str.split(',')[0]
    except:
        print('EXCEPTION : ', _str)
        res = _str
    else:
        return res


def l10n(_str):
    """
    Localization fonction : translate from russian to english"""
    try:
        res = gs.translate(_str.encode("utf8"), target_language="en",
                           source_language="ru")
    except AssertionError:
        print ("assertion error : ")
        print('    {}'.format(_str))
        res = _str
    except urllib.error.HTTPError as e:
        print(*(e, _str), sep = '\n   ')
        res = _str
    return res.encode("utf8").decode("utf8")

def interresting_field(answer):
    res = {"parcels": []}
    for parcel in answer["parcels"] :
        events = parcel["events"]
        trackingNumber = parcel["trackingNumber"]
        l_events = []
        for event in events :
            res_event = {}
            res_event["country"] = event["country"]
            #res_event["detailedLocation"] = l10n(event["detailedLocation"])
            res_event["date"] = translate_date(event["date"])
            res_event["event"] = l10n(clean_html(event["event"]))
            res_event["eventId"] = event["eventId"]
            res_event['location'] = l10n(event["location"])
            l_events.append(res_event)

        tmp = {"events": l_events, "trackingNumber": trackingNumber}
        res["parcels"].append(tmp)
    return res


def get_track_info(l_track_nb):
    track = json.dumps([track_dict(nb) for nb in l_track_nb])
    url = create_url_1(track)
    answer = get_answer(url)
    uid = answer['requestId']
    url = create_url_2(uid)
    answer = get_answer(url)
    #pprint(answer)
    return answer


def get_md5(_object):
    return hashlib.md5(ans.__str__().encode("utf8")).hexdigest()


if __name__ == '__main__':
    track_number = ["RC476805741CN", "RC477597197CN",
                    "RC477408154CN", "RC476805741CN"]
    ans = get_track_info(track_number)
    ans = interresting_field(ans)

    parcels = ans["parcels"]
    last_event_tracking = [(p['events'][-1], p["trackingNumber"]) for p in parcels]

    for event, track_nb in last_event_tracking:
        print(track_nb, ' : ')
        print('   ' + event['date'], event['event'], event['location'], sep=", ")


    print(get_md5(ans))

    #ans = get_track_info(track_number)
    #print(get_md5(ans))
