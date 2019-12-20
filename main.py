import praw
import json
from getpass import getpass
import pathlib, os


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
		print('Welcome /u/%s!'%(reddit.user.me()))
	except:
		print('Error: incorrect username/password.\nExiting...')
		os.sys.exit()
	return reddit

def main():
	banner()
	if cred_check() != True:
		print('''credentials.json does not exist. Refer to the instructions in README.md to create it. 
		reddit-cli will exit now.''')
		os.sys.exit()
	REDDIT = authenticate()
	
if __name__ == '__main__':
	main()
