import praw, json, os, sys
#to add the parent directory to the system path.
sys.path.append('.')

from main import REDDIT

with open('credentials.txt') as creds:
    credentials = json.load(creds)

def get_hot(subreddit):
    subreddit = REDDIT.subreddit(subreddit)
    