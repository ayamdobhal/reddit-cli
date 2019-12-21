import praw
import json
from stdiomask import getpass
import pathlib, os, platform, time
import subreddit.scraper
from choices import choices
from getpass import getpass as gp
import urllib.request

def banner():
	print('''
	██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██████╗██╗     ██╗
	██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝   ██╔════╝██║     ██║
	██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║█████╗██║     ██║     ██║
	██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║╚════╝██║     ██║     ██║
	██║  ██║███████╗██████╔╝██████╔╝██║   ██║      ╚██████╗███████╗██║
	╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚═════╝╚══════╝╚═╝
	''')
	print('''\t\t\t\t\tby /u/AyamDobhal and /u/VineetAhujaX\n\n\n''')

def clrscr():
	if platform.system() == 'Linux':
		os.system('clear')
	elif platform.system() == 'Windows':
		os.system('cls')

def quit():
	print('Exiting...')
	os.sys.exit()

def cred_check():
	creds = pathlib.Path.cwd() /'credentials.json'
	return creds.exists()

def internet_check(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
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
	try:
		if reddit.user.me() == None:
			raise ValueError()
		print('Welcome /u/%s!\n\n'%(reddit.user.me()))
		time.sleep(2)
	except:
		print('Error: incorrect username/password.\nExiting...')
		os.sys.exit()
	return reddit

def main():
	if cred_check() != True:
		print('''credentials.json does not exist. Refer to the instructions in README.md to create it. 
		reddit-cli will exit now.''')
		os.sys.exit()
	if internet_check() == False:
		print('''Internet connection test failed!''')
		print('''Make sure you have a stable internet connection and not using any proxies.''')
		print('''Exiting...''')
		os.sys.exit()
	REDDIT = authenticate()
	while True:
		clrscr()
		banner()
		choice = gp('''Welcome to reddit-cli! What do you want to do today?\n%s\n'''%(choices))
		if choice.lower() == 'h':
			subreddit.scraper.get_hot(REDDIT)
		elif choice.lower() == 'n':
			subreddit.scraper.get_new(REDDIT)
		elif choice.lower() == 'c':
			subreddit.scraper.get_controversial(REDDIT)
		elif choice.lower() == 'r':
			subreddit.scraper.get_rising(REDDIT)
		elif choice.lower() == 't':
			subreddit.scraper.get_top(REDDIT)
		elif choice.lower() == 'q':
			quit()
		else:
			print('Invalid choice! Try again.')
			time.sleep(1)
	
if __name__ == '__main__':
	main()
