import praw
import json
from getpass import getpass


def authenticate():
	with open('credentials.json') as creds:
		credentials = json.load(creds)

	reddit = praw.Reddit(client_id = credentials['client_id'],
				client_secret = credentials['client_secret'],
				user_agent = credentials['user_agent']
				username = input('Enter your reddit username: ')
				password = getpass('Enter your reddit password: ')
			)
	return reddit
