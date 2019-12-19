import praw, json, os
from main import REDDIT

with open('credentials.txt') as creds:
    credentials = json.load(creds)

def get_hot(subreddit):
    subreddit = REDDIT.subreddit(subreddit)
    