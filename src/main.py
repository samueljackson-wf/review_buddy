import argparse
import time
import keyring
import sys

from datetime import datetime, timedelta, timezone
from dateutil import parser as date_parser

from github import Github
from github import Auth

from src.commands.fetch_reviews import FetchReviews
from src.commands.update_access_token import UpdateAccessToken
from src.constants import KEYRING_SERVICE, KEYRING_ACCOUNT


def main():
    parser = argparse.ArgumentParser(
        description='outputs a CSV of PRs that contain reviews or QA from the user'
    )
    parser.add_argument(
        '--edit-access-token',
        action='store_true',
        help='Forces a prompt to update the GitHub access token stored in the Keychain for this script. '
             'If specified, no other actions will be be performed unless also specified.'
    )
    parser.add_argument(
        '--fetch-reviews',
        action='store_true',
        help='Default action. Fetches PRs that contain reviews or QA from the configured user. '
             'Only needs to be specified if --edit-access-token or --edit-config are also specified and reviews should be fetched.'
    )
    parser.add_argument(
        '--starting-at', '-s',
        default=None,
        help='The date of the earliest PR to consider. '
             'Value should be a date String parseable by dateutil.parser. '
             'Defaults to the previous (or current) Monday'
    )
    parser.add_argument(
        '--user', '-u',
        default=None,
        required=True,
        help='The GitHub username to fetch reviews for.'
    )

    args = parser.parse_args()

    force_update_token = args.edit_access_token
    fetch_reviews = args.fetch_reviews

    if force_update_token:
        UpdateAccessToken().apply()
        if not fetch_reviews:
            exit(0)

    token = get_access_token()
    if not token and not force_update_token:
        token = UpdateAccessToken().apply()
    if not token:
        print('Could not get access token', file=sys.stderr)
        exit(1)

    user = args.user.strip()
    if not user:
        print('Invalid username', file=sys.stderr)
        exit(1)

    try:
        starting_at = date_parser.parse(args.starting_at) if args.starting_at else None
    except:
        print('Invalid date format for --starting-at', file=sys.stderr)
        exit(1)

    # Default starting_at to previous monday
    if not starting_at:
        # Previous Monday (weekday=0) = today - today.weekday()
        today = datetime.today()
        starting_at = today - timedelta(days=today.weekday())

    # convert starting_at to UTC
    starting_at_utc = starting_at
    if starting_at_utc.tzinfo != timezone.utc:
        offset = time.localtime().tm_gmtoff
        starting_at_utc = (starting_at - timedelta(seconds=offset)).replace(tzinfo=timezone.utc)

    auth = Auth.Token(token)
    g = Github(auth=auth)

    FetchReviews(user, g, starting_at_utc).apply()


def get_access_token() -> str:
    token = keyring.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
    return '' if not token else token


if __name__ == '__main__':
    main()