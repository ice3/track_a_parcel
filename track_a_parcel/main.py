#!/usr/bin/env python
# -*- coding: utf-8 -*-

from track_a_parcel import Tracker, get_md5

if __name__ == '__main__':
    track_number = ["RC476805741CN", "RC477597197CN",
                    "RC477408154CN", "RC476805741CN"]
    tracker = Tracker()
    ans = tracker.track(track_number)

    parcels = ans["parcels"]
    last_event_tracking = [(p['events'][-1], p["trackingNumber"]) for p in parcels]

    for event, track_nb in last_event_tracking:
        print(track_nb, ' : ')
        print('   ' + event['date'], event['event'], event['location'], sep=", ")


    print(get_md5(ans))
