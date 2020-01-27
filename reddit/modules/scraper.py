# Copyright (C) 2020 AyamDobhal.
#
# Licensed under the GNU General Public License v3.0;
#
# You may not use this file except in compliance with the license.
#
# If you think you will copy my hardwork and get away with it, DMCA welcomes you!

import os, sys, time, platform
import webbrowser
from contextlib import suppress
from getpass import getpass as gp
from reddit.modules.login import authenticate

# to add the parent directory to the system path.
sys.path.append(".")

import praw


def clrscr():
    """A function to clear the previous output."""
    if platform.system().lower() == "linux":
        os.system("clear")
    elif platform.system().lower() == "windows":
        os.system("cls")


def banner():
    """A function to print the banner/logo."""
    print(
        """
	██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██████╗██╗     ██╗
	██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝   ██╔════╝██║     ██║
	██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║█████╗██║     ██║     ██║
	██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║╚════╝██║     ██║     ██║
	██║  ██║███████╗██████╔╝██████╔╝██║   ██║      ╚██████╗███████╗██║
	╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚═════╝╚══════╝╚═╝
	"""
    )
    print("""\t\t\t\t\t\t\tby /u/AyamDobhal\n\n\n""")


# initializing the reddit class
clrscr()
banner()
reddit = authenticate()


def quit():
    """A function to exit the script."""
    print("Exiting...")
    os.sys.exit()


def LinkHandler(link):
    """A function to handle links across operating systems."""
    if "ANDROID_DATA" in os.environ:
        os.system("termux-open-url " + link)
    else:
        webbrowser.open_new_tab(link)


def init_subreddit(reddit, subreddit):
    """A function to initialize the reddit.subreddit instance."""
    try:
        subreddit = reddit.subreddit(subreddit)
        print("You are browsing /r/%s" % subreddit.fullname)
        clrscr()
        return subreddit
    except:
        print("subreddit does not exist. \nReturning to menu in 2 seconds...")
        time.sleep(2)
        suppress(Exception)


class Scraper:
    """A class that has subclasses for utilizing methods provided by praw."""

    class User:
        """A class to utilize the reddit.user instance."""

        def __init__(self, user, limit=10):
            self.user = user
            self.blocked = user.blocked()
            self.karma = user.karma()
            self.subreddits = user.subreddits()
            self.contributor_subreddit = user.contributor_subreddit()
            self.preferences = user.preferences()
            self.me = user.me()

        def BlockedUsers(self):
            """A function to output the usernames of the users blocked by the authenticated user."""
            if len(self.blocked()) == 0:
                print("You have not blocked any user.")
            else:
                for usr in self.blocked():
                    print("\t" + str(usr))
            gp("Enter any key to go back.")
            Scraper.User.main(self)

        def Preferences(self):
            """A function to output the preferences of the authenticated user."""
            clrscr()
            banner()
            print("Preferences:")
            prefs = []
            for pref, option in self.preferences().items():
                prefs.append([pref, option])
            for i in range(len(prefs) // 4):
                print(prefs[i][0], ":", prefs[i][1])
            choice = gp(
                """Enter your choice.[Y to see more prefs, U if you want to update any pref, any other key to return to profile]"""
            )
            if choice.lower() == "y":
                for i in range(len(prefs) // 4, len(prefs) // 2):
                    print(prefs[i][0], ":", prefs[i][1])
            elif choice.lower() == "u":
                print("redirecting to reddit.com to update prefs...")
                time.sleep(1)
                LinkHandler("https://reddit.com/prefs")
                Scraper.User.main(self)
            else:
                Scraper.User.main(self)
            choice = gp(
                "Enter you choice.[U if you want to update a pref, any other key to return to profile.]"
            )
            if choice.lower() == "y":
                for i in range(len(prefs) // 2, len(prefs) // 2 + len(prefs) // 4):
                    print(prefs[i][0], ":", prefs[i][1])
            elif choice.lower() == "u":
                print("redirecting to reddit.com to update prefs...")
                time.sleep(1)
                LinkHandler("httpe://reddit.com/prefs")
                Scraper.User.main(self)
            else:
                Scraper.User.main(self)
            choice = gp(
                "Enter your choice.[Y to see more prefs, U if you want to update any pref, any other key to return to profile.]"
            )
            if choice.lower() == "y":
                for i in range(len(prefs) // 2 + len(prefs) // 4, -1):
                    print(prefs[i][0], ":", prefs[i][1])
            elif choice.lower() == "u":
                print("redirecting to reddit.com to update prefs...")
                time.sleep(1)
                LinkHandler("https://reddit.com/prefs")
                Scraper.User.main(self)
            else:
                Scraper.User.main(self)

        def Subscribed(self):
            """A function to output the subreddits the authenticated user has subscribed to."""
            for subreddit in self.subreddits():
                print("\t", subreddit)
            choice = gp("\n\nEnter [Y] if you want to open a subreddit.")
            if choice.lower() == "y":
                subreddit = input("Enter the name of the subreddit: ")
                Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
            else:
                Scraper.User.main(self)

        def main(self):
            """The main menu for the user class."""
            link_karma_count = 0
            comment_karma_count = 0
            for item in self.karma().values():
                link_karma_count += item["link_karma"]
                comment_karma_count += item["comment_karma"]
            clrscr()
            banner()
            print("Hello /u/" + str(self.me()))
            print(
                "Karma count --> link karma : %d comment karma : %d\n\n"
                % (link_karma_count, comment_karma_count)
            )
            choice = gp(
                """Enter your choice to continue:
[B] to display users you have blocked.
[P] to display account preferences.
[S] to display subreddits you have subscribed to.
[Q] to go return to main menu."""
            )

            if choice.lower() == "b":
                Scraper.User.BlockedUsers(self)
            elif choice.lower() == "p":
                Scraper.User.Preferences(self)
            elif choice.lower() == "s":
                Scraper.User.Subscribed(self)
            elif choice.lower() == "q":
                print("Returning to main menu as requested...")
                time.sleep(1)
            else:
                print("Invalid choice entered. Try again...")
                time.sleep(1)
                Scraper.User.main(self)

    class Subreddits:
        """A class to utilize the reddit.subreddits instance."""

        def __init__(self, subreddits):
            self.new = subreddits.new(limit=10)
            self.popular = subreddits.popular(limit=10)
            self.recommended = subreddits.recommended(limit=10)
            self.search = subreddits.search(limit=10)
            self.search_by_name = subreddits.search_by_name(limit=10)
            self.search_by_topic = subreddits.search_by_topic(limit=10)

        def NewSubreddits(self):
            """A function to output 10 newest subreddits."""
            print("Newest subreddits are:")
            for subreddit in self.new(limit=10):
                print("\t", subreddit)
            choice = gp("\n\nEnter [Y] if you want to open a subreddit.")
            if choice.lower() == "y":
                subreddit = input("Enter the name of the subreddit:")
                Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
            else:
                Scraper.Subreddits.main(self)

        def PopularSubreddits(self):
            """A function to output 10 most popular subreddits."""
            print("Most popular subreddits right now are:")
            for subreddit in self.popular(limit=10):
                print("\t", subreddit)
            choice = gp("\n\nEnter [Y] if you want to open a subreddit.")
            if choice.lower() == "y":
                subreddit = input("Enter the name of the subreddit: ")
                Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
            else:
                Scraper.Subreddits.main(self)

        def Search(self):
            """A function to search for subreddits by name/description."""
            query = input(
                "Enter the keyword in the name/description of the subreddit you want to find:"
            )
            print("Search results:")
            try:
                for subreddit in self.search(query, limit=10):
                    print("\t", subreddit)
            except:
                print("Subreddit not found!")
                time.sleep(1)
                Scraper.Subreddits.main(self)
            choice = gp("\nEnter [Y] if you want to open any of the above subreddits.")
            if choice.lower() == "y":
                subreddit = input("Enter the name of the subreddit:")
                Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
            else:
                Scraper.Subreddits.main(self)

        def SearchByName(self):
            """A function to search for subreddits by name."""
            query = input("Enter the name of the subreddit you want to search for:")
            print("Search results:")
            try:
                for subreddit in self.search_by_name(query):
                    print("\t", subreddit)
            except:
                print("Subreddit not found!")
                time.sleep(1)
                Scraper.Subreddits.main(self)
            choice = gp("\nEnter [Y] if you want to open any of the above subreddits.")
            if choice.lower() == "y":
                subreddit = input("Enter the name of the subreddit:")
                Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
            else:
                Scraper.Subreddits.main(self)

        def SearchByTopic(self):
            """A function to search for subreddits by topic."""
            query = input("Enter the topic of the subreddit you want to search:")
            print("Search results:")
            try:
                for subreddit in self.search_by_topic(query):
                    print("\t", subreddit)
            except:
                print("Subreddit not found!")
                time.sleep(1)
                Scraper.Subreddits.main(self)
            choice = gp(
                "\nEnter [Y] if you want to open any of the above subreddits.\n"
            )
            if choice.lower() == "y":
                subreddit = input("Enter the name of the subreddit: ")
                Scraper.Subreddit.main(init_subreddit(reddit, subreddit))
            else:
                Scraper.Subreddits.main(self)

        def main(self):
            """The main menu for the subreddits class."""
            clrscr()
            banner()
            choice = gp(
                """What do you want to do?
[N] to show new subreddits.
[P] to show popular subreddits.
[S] to search for a subreddit by name/description.
[B] to search for a subreddit by name.
[T] to search for a subreddit by topic.
[Q] to return to main menu\n"""
            )
            if choice.lower() == "n":
                Scraper.Subreddits.NewSubreddits(self)
            elif choice.lower() == "p":
                Scraper.Subreddits.PopularSubreddits(self)
            elif choice.lower() == "s":
                Scraper.Subreddits.Search(self)
            elif choice.lower() == "b":
                Scraper.Subreddits.SearchByName(self)
            elif choice.lower() == "t":
                Scraper.Subreddits.SearchByTopic(self)
            elif choice.lower() == "q":
                print("Returning to main menu as requested...")
                time.sleep(1)
            else:
                print("Invalid choice entered. Try again...")
                time.sleep(1)
                Scraper.Subreddits.main(self)

    class Subreddit:
        """A class to utilize the reddit.subreddit instance."""

        def show_posts(self, sort):
            """A function to show 10 submissions from the subreddit."""
            print(
                "Fetching 10 {} submissions from {}... \n\n".format(
                    sort["txt"], self.display_name
                )
            )
            for submission in sort["func"](limit=10):
                print(submission.title)
                print("score={}".format(submission.score))
                choice = gp(
                    "[y] to open this submission in your "
                    + "browser, [q] to go back to menu, or "
                    + "any other key to skip to the next post\n"
                ).lower()
                if choice == "y":
                    LinkHandler("https://redd.it/" + submission.id)
                    time.sleep(2)
                elif choice == "q":
                    break
            Scraper.Subreddit.main(self)

        def main(self):
            """The main menu for the subreddit class."""
            clrscr()
            banner()
            print("Welcome to /r/{}".format(self.display_name))
            print("Id of subreddit: ".format(self.id))
            print("No. of subscribers: {}".format(self.subscribers))
            if self.user_is_banned:
                print("You're banned from this subreddit.")
            if self.user_is_moderator:
                print("You're a moderator of this subreddit.")
            if self.user_is_subscriber:
                print("You're subscribed to this subreddit.")
            choice = gp(
                "\nWhat do you want to do here?\n"
                + "[h] to display hot submissions.\n"
                + "[n] to display new submissions.\n"
                + "[t] to display top submissions.\n"
                + "[q] to go back to main menu.\n"
            ).lower()
            sort_types = {
                "h": {"txt": "hot", "func": self.hot},
                "t": {"txt": "top", "func": self.top},
                "n": {"txt": "new", "func": self.new},
            }
            if choice in sort_types:
                Scraper.Subreddit.show_posts(self, sort_types[choice])
            elif choice == "q":
                print("Returning to main menu as requested...")
                time.sleep(1)
            else:
                print("Invalid choice entered. Try again...")
                time.sleep(1)
                Scraper.Subreddit.main(self)

    class Inbox:
        """A class to utilize the reddit.inbox instance."""

        def __init__(self):
            self.mark_read = self.mark_read()
            self.unread = self.unread()
            self.mark_unread = self.mark_unread()

        def MarkRead(self, msg):
            """A function to mark an inbox message as read."""
            self.mark_read(msg)

        def Unread(self):
            """A function to output the unread messages of the user."""
            unread = []
            for item in self.unread():
                unread.append(item)
            if len(unread) == 0:
                print("You have no unread messages.")
                time.sleep(1)
                Scraper.Inbox.main(self)
            mark_read = []
            for msg in unread:
                print("Message id: ", str(msg))
                print("Sent by:", msg.author.name)
                print("Subject:", msg.subject)
                print("Body:", msg.body)
                choice = gp(
                    """Enter [Y] if you want to mark this message as read. 
[B] if you want to block the sender.
[D] if you want to delete this message.
Any other key to continue."""
                )
                if choice.lower() == "y":
                    mark_read.append(msg)
                elif choice.lower() == "b":
                    msg.author.block()
                elif choice.lower() == "d":
                    msg.delete()
                Scraper.Inbox.MarkRead(self, mark_read)
                Scraper.Inbox.main(self)

        def main(self):
            """The main menu for the inbox class."""
            clrscr()
            banner()
            print("Welcome to inbox.")
            choice = gp(
                """Enter your choice.
[U] to view unread messages.
[Q] to quit to main menu."""
            )
            if choice.lower() == "u":
                Scraper.Inbox.Unread(self)
            elif choice.lower() == "q":
                print("Returning to main menu as reqested...")
                time.sleep(1)
            else:
                print("Invalid choice entered. Try again...")
                time.sleep(1)
                Scraper.Inbox.main(self)
