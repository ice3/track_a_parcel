#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from track_a_parcel import Tracker, get_md5, load_parcels

    last_event_tracking = [(p['events'][-1], p["trackingNumber"])
                           for p in parcels]

    for event, track_nb in last_event_tracking:
        description, command, seller = info_track[track_nb]
        print('[{}]'.format(track_nb), description,
              '({}, {})'.format(seller, command), sep=' ')
        print('  -> ' + event['date'], event['event'], event['location'],
              sep=", ")
        print()


if __name__ == '__main__':
    info_track = load_parcels("./data/mat.txt")
    tracker = Tracker()
    ans = tracker.track(list(info_track))
    parcels = ans["parcels"]
    view(parcels)
    print(get_md5(ans))
