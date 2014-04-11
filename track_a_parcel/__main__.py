#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os

from track_a_parcel import Tracker, get_md5, load_parcels
from command_line import create_args

def view(parcels, info_track):
    last_event_tracking = [(p['events'][-1], p["trackingNumber"])
                           for p in parcels]

    for event, track_nb in last_event_tracking:
        description, command, seller = info_track[track_nb]
        print('[{}]'.format(track_nb), description,
              '({}, {})'.format(seller, command), sep=' ')
        print('  -> ' + event['date'], event['event'], event['location'],
              sep=", ")
        print()


def track(info_track):
    tracker = Tracker()
    ans = tracker.track(list(info_track))
    parcels = ans["parcels"]
    return parcels


def main(user):
    print("Tracking parcels for {}".format(user))
    user_parcelle = "./data/{}/parcelle.txt".format(user)
    if not os.path.isfile(user_parcelle):
        mess = "User {} does not have any parcels to track".format(user)
        print(mess)
    else:
        info_track = load_parcels(user_parcelle)
        parcels = track(info_track)
        print(parcels)
        view(parcels, info_track)


if __name__ == '__main__':
    args = create_args()
    users = args.user
    [main(user) for user in users]
