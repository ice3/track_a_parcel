#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os

from track_a_parcel import Tracker, get_md5, load_parcels
from command_line import create_args


def last_n_events(parcels, n):
    nb_events = -n  # we want the N last events
    # get the last events
    tmp = [(p['events'][nb_events:], p["trackingNumber"]) for p in parcels]
    # reverse : last events first
    last_events_tracking = [(e[::-1], trNb) for e, trNb in tmp]
    return last_events_tracking


def view_info(parcels, info_track, nb_events):
    for events, track_nb in last_n_events(parcels, nb_events):
        description, command, seller = info_track[track_nb]
        print('[{}]'.format(track_nb), description,
              '({}, {})'.format(seller, command), sep=' ')
        for event in events:
            print('  -> ' + event['date'], event['event'], event['location'],
                  sep=", ")
        print()


def view_loading(info_track):
    print('Found {} parcels :'.format(len(info_track)))
    print(*['  * ' + i for i in list(info_track)], sep=' \n')


def track(info_track):
    tracker = Tracker()
    ans = tracker.track(list(info_track))
    parcels = ans["parcels"]
    return parcels


def main(user, nb_events):
    print("Tracking parcels for {}".format(user))
    user_parcelle = "./data/{}/parcelle.txt".format(user)
    if not os.path.isfile(user_parcelle):
        mess = "User {} does not have any parcels to track".format(user)
        print(mess)
    else:
        info_track = load_parcels(user_parcelle)
        view_loading(info_track)
        parcels = track(info_track)
        view_info(parcels, info_track, nb_events)


if __name__ == '__main__':
    args = create_args()

    if args.test_view:
        from view2_data import data, info_track
        view_info(data, info_track, args.nb_events)
        import sys
        sys.exit(1)

    [main(user, args.nb_events) for user in args.users]


