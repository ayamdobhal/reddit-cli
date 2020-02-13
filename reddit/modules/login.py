# Copyright (C) 2020 AyamDobhal.
#
# Licensed under the GNU General Public License v3.0;
#
# You may not use this file except in compliance with the license.
#
# If you think you will copy my hardwork and get away with it, DMCA welcomes you!

import json
import os
import pathlib
import praw
import prawcore
import socket

from getpass import getpass


def cred_check():
    """A function to check whether credentials.json exists or not."""
    creds = pathlib.Path.cwd() / "credentials.json"
    return creds.exists()


def internet_check():
    """A function to test the connectivity to https://reddit.com."""
    try:
        socket.create_connection(("www.reddit.com", 443))
        return True
    except OSError:
        return False


def authenticate():
    """A function to authenticate the user and return the reddit instance."""
    if not cred_check():
        print("""credentials.json does not exist.""")
        print("""refer to instructions and create it""")
        os.sys.exit()
    try:
        with open("credentials.json") as creds:
            credentials = json.load(creds)

        reddit = praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            user_agent=credentials["user_agent"],
            username=input("Enter your reddit username: "),
            password=getpass("Enter your reddit password: "),
        )
        if not reddit.user.me():
            os.sys.exit()
        print("Welcome /u/%s!\n\n" % (reddit.user.me()))
        return reddit
    except prawcore.exceptions.OAuthException:
        print("Incorrect username/password. Try again...")
        os.sys.exit()
