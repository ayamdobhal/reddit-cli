# Copyright (C) 2020 AyamDobhal.
#
# Licensed under the GNU General Public License v3.0;
#
# You may not use this file except in compliance with the license.
#
# If you think you will copy my hardwork and get away with it, DMCA welcomes you!

import datetime
import json
import jwt
import os
import pathlib
import praw
import prawcore
import socket

from base64 import b64encode, b64decode
from getpass import getpass


def gen_jwt():
    username = input("Enter your reddit username: ")
    password = getpass("Enter your reddit password: ")
    secret = getpass("Enter a secret key(Automatically loaded): ")
    token = jwt.encode({'user': username, 'pass': password,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                       secret)

    with open("jwt.json", "w+") as jwtfile:
        jwtfile.write(json.dumps({'token': token.decode("UTF-8"),
                                  'secret': b64encode(bytes(secret, "UTF-8")).decode("UTF-8")}))

    return {'user': username, 'pass': password}


def load_jwt():
    try:
        with open("jwt.json", "r") as jwtfile:
            jwtjson = json.load(jwtfile)
            data = jwt.decode(jwtjson['token'], b64decode(bytes(jwtjson['secret'], "UTF-8").decode("UTF-8")))
            return data
    except (jwt.ExpiredSignatureError, FileNotFoundError):
        print('Token Error!\n')
        return gen_jwt()


def cred_check():
    """A function to check whether credentials.json exists or not."""
    creds = pathlib.Path.cwd() / "credentials.json"
    return creds.exists()


def jwt_check():
    jwtcreds = pathlib.Path.cwd() / "jwt.json"
    return jwtcreds.exists()


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

        user_creds = load_jwt()

        reddit = praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            user_agent=credentials["user_agent"],
            username=user_creds['user'],
            password=user_creds['pass'],
        )
        if not reddit.user.me():
            os.sys.exit()
        print("Welcome /u/%s!\n\n" % (reddit.user.me()))
        return reddit
    except prawcore.exceptions.OAuthException:
        print("Incorrect username/password. Try again...")
        gen_jwt()
        return authenticate()
