import json
import os, platform, time
from getpass import getpass as gp
from reddit.modules.login import cred_check, internet_check
from reddit.modules.scraper import Scraper, banner, clrscr, quit, init_subreddit, reddit

try:
    import praw, stdiomask
except ImportError:
    print("ImportError: Some dependencies are not installed.")
    print("Enter 'pip install -r requirements.txt' to install them.")
    quit()

def main():
    """The main menu for reddit-cli."""
    while True:
        clrscr()
        banner()
        choice = gp(
            """Welcome to reddit-cli. What action do you want to perform?
[P] to display profile.
[S] to search for subreddits.
[B] to browse a subreddit.
[I] to open inbox.
[Q] to quit.\n"""
        )
        if choice.lower() == "p":
            Scraper.User.main(reddit.user)
        elif choice.lower() == "s":
            Scraper.Subreddits.main(reddit.subreddits)
        elif choice.lower() == "b":
            subreddit = input("Enter the name of the subreddit:")
            Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
        elif choice.lower() == "i":
            Scraper.Inbox.main(reddit.inbox)
        elif choice.lower() == "q":
            quit()
        else:
            print("Invalid choice entered. Try again...")
            time.sleep(1)


if __name__ == "__main__":
    main()
