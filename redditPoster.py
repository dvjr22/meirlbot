# Set up praw Oauth2 stuff via: https://github.com/x89/Shreddit/blob/master/get_secret.py

import os
import sys
import praw
import random
import argparse
import yaml

from re import sub
from datetime import datetime, timedelta
from praw.errors import (InvalidUser, InvalidUserPass, RateLimitExceeded, HTTPException, OAuthAppRequired)
from praw.objects import Comment, Submission

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c',
    '--config',
    help="config file to use for credentials"
)
args = parser.parse_args()

if args.config:
    # A correct config file was given
    config_file = args.config
else:
    # Else try with a default file
    config_file = 'praw.ini'
with open(config_file, 'r') as fh:
    config = yaml.safe_load(fh)
if config is None:
    raise Exception("No config options passed!")

r = praw.Reddit(user_agent="bigteaisbest")

try:
    # Try logging in with a OAuth2
    r.refresh_access_information()
except (HTTPException, OAuthAppRequired) as e:



r.upload_image('me_irl', './images/test.png')
