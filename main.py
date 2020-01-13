import praw
import json
from stdiomask import getpass
import pathlib, os, platform, time
from getpass import getpass as gp
import urllib.request
from login import authenticate, cred_check, internet_check
from subreddit.scraper import Scraper, banner, clrscr, quit, init_subreddit

def main():
	if cred_check() != True:
		print('''credentials.json does not exist. Refer to the instructions in README.md to create it. 
		reddit-cli will exit now.''')
		os.sys.exit()

	#initializing the reddit class
	username = input('Enter your reddit usermame:')
	password = getpass('Enter your reddit password:')
	reddit = authenticate(username,password)
	
	while True:
		clrscr()
		banner()
		choice = gp('''Welcome to reddit-cli. What action do you want to perform?
[P] to display profile.
[S] to search for subreddits.
[B] to browse a subreddit.
[Q] to quit.''')
		if choice.lower() == 'p':
			Scraper.User.main(reddit.user)
		elif choice.lower() == 's':
			Scraper.Subreddits.main(reddit.subreddits)
		elif choice.lower() == 'b':
			subreddit = input('Enter the name of the subreddit:')
			Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
		elif choice.lower() == 'q':
			quit()
		else:
			print('Invalid choice entered. Try again...')
			time.sleep(1)
if __name__ == '__main__':
	main()
