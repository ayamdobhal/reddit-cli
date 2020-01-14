import json, os, pathlib
import praw
from stdiomask import getpass
import urllib.request

def cred_check():
	creds = pathlib.Path.cwd() /'credentials.json'
	return creds.exists()

def internet_check():
    try:
        urllib.request.urlopen('https://reddit.com/')  
        return True
    except:
        return False

def authenticate():
	try:
		with open('credentials.json') as creds:
			credentials = json.load(creds)

		reddit = praw.Reddit(client_id = credentials['client_id'],
					client_secret = credentials['client_secret'],
					user_agent = credentials['user_agent'],
					username = input('Enter your reddit username:'),
					password = getpass('Enter your reddit password:')
				)
		if reddit.user.me() == None:
			os.sys.exit()
		print('Welcome /u/%s!\n\n'%(reddit.user.me()))
		return reddit
	except:
		print('Incorrect username/password. Try again...')
		os.sys.exit()