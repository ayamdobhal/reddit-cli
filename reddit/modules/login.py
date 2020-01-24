import json, os, pathlib
import praw
from stdiomask import getpass
import urllib.request


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

        reddit = praw.Reddit(
            client_id = credentials["client_id"],
            client_secret = credentials["client_secret"],
            user_agent = credentials["user_agent"],
            username = input("Enter your reddit username: "),
            password = getpass("Enter your reddit password: "),
        )
        if reddit.user.me() == None:
            os.sys.exit()
        print("Welcome /u/%s!\n\n" % (reddit.user.me()))
        return reddit
    except:
        print("Incorrect username/password. Try again...")
        os.sys.exit()
