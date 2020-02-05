# Copyright (C) 2020 AyamDobhal.
#
# Licensed under the GNU General Public License v3.0;
#
# You may not use this file except in compliance with the license.
#
# If you think you will copy my hardwork and get away with it, DMCA welcomes you!

import json, os, pathlib
import praw
from stdiomask import getpass
import urllib.request
from hashlib import md5


def cred_check():
    """A function to check whether credentials.json exists or not."""
    creds = pathlib.Path.cwd() / "credentials.json"
    return creds.exists()


def internet_check():
    """A function to test the connectivity to https://reddit.com."""
    try:
        urllib.request.urlopen("https://reddit.com/")
        return True
    except:
        return False


def authenticate():
    """A function to authenticate the user and return the reddit instance."""
    if cred_check() != True:
        print("""credentials.json does not exist.""")
        print("""refer to instructions and create it""")
        os.sys.exit()
    try:
        with open("credentials.json") as creds:
            credentials = json.load(creds)
        try:
            with open('login.txt') as login:
                log = login.readlines()
                usrname = log[0]
                pwd = log[1]
        except:
            usrname = input('Enter your username: ')
            password = getpass('Enter your password: ')
            choice = input("Do you want to save your login information?[Y for yes]")
            if choice.lower() == 'y':
                with open('login.txt','w') as login:
                    login.write(usrname+'\n'+pwd)
        
        reddit = praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            user_agent=credentials["user_agent"],
            username = usrname,
            password = pwd
        )
        
        if reddit.user.me() == None:
            os.sys.exit()
        print("Welcome /u/%s!\n\n" % (reddit.user.me()))
        return reddit
    except:
        print("Incorrect username/password. Try again...")
        os.sys.exit()
