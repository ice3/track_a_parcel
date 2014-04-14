import argparse

def create_args():
    parser = argparse.ArgumentParser(description='Track a parcel.')
    parser.add_argument("user", nargs='+')
    parser.add_argument("--cron", action='store_true')
    parser.add_argument("--test_view", action="store_true")
    parser.add_argument('--nb_events', type=int, default='1')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = create_args()
    print(args.user)
    print(args.cron)
