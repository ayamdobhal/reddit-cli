import json, os, pathlib
import praw
from stdiomask import getpass

def cred_check():
	creds = pathlib.Path.cwd() /'credentials.json'
	return creds.exists()

def internet_check():
    try:
        urllib.request.urlopen('https://gooogle.com')  
        return True
    except:
        return False

def authenticate():
	with open('credentials.json') as creds:
		credentials = json.load(creds)

	reddit = praw.Reddit(client_id = credentials['client_id'],
				client_secret = credentials['client_secret'],
				user_agent = credentials['user_agent'],
				username = input('Enter your reddit username: '),
				password = getpass('Enter your reddit password: ')
			)
	if reddit.user.me() == None:
		raise ValueError()
	print('Welcome /u/%s!\n\n'%(reddit.user.me()))

	return reddit