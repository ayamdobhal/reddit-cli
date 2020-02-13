# Copyright (C) 2020 AyamDobhal.
#
# Licensed under the GNU General Public License v3.0;
#
# You may not use this file except in compliance with the license.
#
# If you think you will copy my hardwork and get away with it, DMCA welcomes you!

import time
from getpass import getpass as gp
from reddit import conf
from reddit.modules.login import authenticate
from reddit.modules.scraper import Scraper, Subreddit, banner, clrscr, quit_app

try:
    import praw
except ImportError:
    print("ImportError: Some dependencies are not installed.")
    print("Enter 'pip install -r requirements.txt' to install them.")
    quit_app()


def main():
    """The main menu for reddit-cli."""
    clrscr()
    banner()
    reddit = authenticate()
    scraper = Scraper(reddit)
    conf.CHOICE = gp(
        """Welcome to reddit-cli. What action do you want to perform?
[P] to display profile.
[S] to search for subreddits.
[B] to browse a subreddit.
[I] to open inbox.
[Q] to quit.\n"""
    )
    while True:
        if conf.CHOICE.lower() == "p":
            scraper.user.main()
        elif conf.CHOICE.lower() == "s":
            scraper.subreddits.main()
        elif conf.CHOICE.lower() == "b":
            subreddit = Subreddit(input("Enter the name of the subreddit:"), scraper)
            subreddit.main()
        elif conf.CHOICE.lower() == "i":
            scraper.inbox()
        elif conf.CHOICE.lower() == "q":
            quit_app()
        else:
            print("Invalid choice entered. Try again...")
            time.sleep(1)


if __name__ == "__main__":
    main()
