import praw
import json
from stdiomask import getpass
import pathlib, os, platform
import subreddit.scraper
from choices import choices


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
		print('Welcome /u/%s!\n\n'%(reddit.user.me()))
	except:
		print('Error: incorrect username/password.\nExiting...')
		os.sys.exit()
	return reddit

def main():
	if cred_check() != True:
		print('''credentials.json does not exist. Refer to the instructions in README.md to create it. 
		reddit-cli will exit now.''')
		os.sys.exit()
	REDDIT = authenticate()
	while True:
		clrscr()
		banner()
		choice = input('''Welcome to reddit-cli! What do you want to do today?\n%s\n'''%(choices))
		if choice.lower() == 'h':
			subreddit.scraper.get_hot(REDDIT)
		elif choice.lower() == 'q':
			quit()
		else:
			raise Warning('Inavlid choice!\n\n')
	
if __name__ == '__main__':
	main()
