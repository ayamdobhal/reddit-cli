# Copyright (C) 2020 AyamDobhal.
#
# Licensed under the GNU General Public License v3.0;
#
# You may not use this file except in compliance with the license.
#
# If you think you will copy my hardwork and get away with it, DMCA welcomes you!

import os
import sys
import time
import platform
import webbrowser

from contextlib import suppress
from getpass import getpass as gp
from reddit import conf

# to add the parent directory to the system path.
sys.path.append(".")


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


def print_main():
    clrscr()
    banner()
    conf.CHOICE = gp(
        """
[P] to display profile.
[S] to search for subreddits.
[B] to browse a subreddit.
[I] to open inbox.
[Q] to quit.\n"""
    )


def quit_app():
    """A function to exit the script."""
    print("Exiting...")
    os.sys.exit()


def link_handler(link):
    """A function to handle links across operating systems."""
    if "ANDROID_DATA" in os.environ:
        os.system("termux-open-url " + link)
    else:
        webbrowser.open_new_tab(link)


class Scraper:
    """A class that has subclasses for utilizing methods provided by praw."""
    def __init__(self, reddit):
        self.reddit = reddit
        self.user = User(self)
        self.subreddits = Subreddits(self)
        self.inbox = Inbox(self)


class User:
    def __init__(self, scraper: Scraper):
        self.scraper = scraper
        self.user = scraper.reddit.user

    """A class to utilize the reddit.user instance."""
    def blocked_users(self):
        """A function to output the usernames of the users blocked by the authenticated user."""
        if len(self.user.blocked()) == 0:
            print("You have not blocked any user.")
        else:
            for usr in self.user.blocked():
                print("\t" + str(usr))
        gp("Enter any key to go back.")
        self.main()

    def preferences(self):
        """A function to output the preferences of the authenticated user."""
        clrscr()
        banner()
        print("Preferences:")
        prefs = []
        for pref, option in self.user.preferences().items():
            prefs.append([pref, option])
        for i in range(len(prefs) // 4):
            print(prefs[i][0], ":", prefs[i][1])
        choice = gp(
            "Enter your choice.[Y to see more prefs, U if you want to update any pref,"
            " any other key to return to profile]"
        )
        if choice.lower() == "y":
            for i in range(len(prefs) // 4, len(prefs) // 2):
                print(prefs[i][0], ":", prefs[i][1])
        elif choice.lower() == "u":
            print("redirecting to reddit.com to update prefs...")
            time.sleep(1)
            link_handler("https://reddit.com/prefs")
            self.main()
        else:
            self.main()
        choice = gp(
            "Enter you choice.[U if you want to update a pref, any other key to return to profile.]"
        )
        if choice.lower() == "y":
            for i in range(len(prefs) // 2, len(prefs) // 2 + len(prefs) // 4):
                print(prefs[i][0], ":", prefs[i][1])
        elif choice.lower() == "u":
            print("redirecting to reddit.com to update prefs...")
            time.sleep(1)
            link_handler("httpe://reddit.com/prefs")
            self.main()
        else:
            self.main()
        choice = gp(
            "Enter your choice.[Y to see more prefs, U if you want to update any pref,"
            " any other key to return to profile.]"
        )
        if choice.lower() == "y":
            for i in range(len(prefs) // 2 + len(prefs) // 4, -1):
                print(prefs[i][0], ":", prefs[i][1])
        elif choice.lower() == "u":
            print("redirecting to reddit.com to update prefs...")
            time.sleep(1)
            link_handler("https://reddit.com/prefs")
            self.main()
        else:
            self.main()

    def subscribed(self):
        """A function to output the subreddits the authenticated user has subscribed to."""
        for subreddit in self.user.subreddits():
            print("\t", subreddit)
        choice = gp("\n\nEnter [Y] if you want to open a subreddit.")
        if choice.lower() == "y":
            subreddit = Subreddit(input("Enter the name of the subreddit: "), self.scraper)
            subreddit.main()
        else:
            self.main()

    def main(self):
        """The main menu for the user class."""
        link_karma_count = 0
        comment_karma_count = 0
        for item in self.user.karma().values():
            link_karma_count += item["link_karma"]
            comment_karma_count += item["comment_karma"]
        clrscr()
        banner()
        print("Hello /u/" + str(self.user.me()))
        print(
            "Karma count --> link karma : %d comment karma : %d\n\n"
            % (link_karma_count, comment_karma_count)
        )
        choice = gp(
            """Enter your choice to continue:
[B] to display users you have blocked.
[P] to display account preferences.
[S] to display subreddits you have subscribed to.
[Q] to go return to main menu.
"""
        )

        if choice.lower() == "b":
            self.blocked_users()
        elif choice.lower() == "p":
            self.preferences()
        elif choice.lower() == "s":
            self.subscribed()
        elif choice.lower() == "q":
            print("Returning to main menu as requested...")
            print_main()
        else:
            print("Invalid choice entered. Try again...")
            time.sleep(1)
            self.main()


class Subreddits:
    """A class to utilize the reddit.subreddits instance."""

    def __init__(self, scraper: Scraper):
        self.scraper = scraper
        self.subreddits = scraper.reddit.subreddits

    def new_subreddit(self):
        """A function to output 10 newest subreddits."""
        print("Newest subreddits are:")
        for subreddit in self.subreddits.new(limit=10):
            print("\t", subreddit)
        choice = gp("\n\nEnter [Y] if you want to open a subreddit.")
        if choice.lower() == "y":
            subreddit = Subreddit(input("Enter the name of the subreddit:"), self.scraper)
            subreddit.main()
        else:
            self.main()

    def popular_subreddits(self):
        """A function to output 10 most popular subreddits."""
        print("Most popular subreddits right now are:")
        for subreddit in self.subreddits.popular(limit=10):
            print("\t", subreddit)
        choice = gp("\n\nEnter [Y] if you want to open a subreddit.")
        if choice.lower() == "y":
            subreddit = Subreddit(input("Enter the name of the subreddit: "), self.scraper)
            subreddit.main()
        else:
            self.main()

    def search(self):
        """A function to search for subreddits by name/description."""
        query = input(
            "Enter the keyword in the name/description of the subreddit you want to find:"
        )
        print("Search results:")
        try:
            for subreddit in self.subreddits.search(query, limit=10):
                print("\t", subreddit)
        except:
            print("Subreddit not found!")
            time.sleep(1)
            self.main()
        choice = gp("\nEnter [Y] if you want to open any of the above subreddits.")
        if choice.lower() == "y":
            subreddit = Subreddit(input("Enter the name of the subreddit:"), self.scraper)
            subreddit.main()
        else:
            self.main()

    def search_by_name(self):
        """A function to search for subreddits by name."""
        query = input("Enter the name of the subreddit you want to search for:")
        print("Search results:")
        try:
            for subreddit in self.subreddits.search_by_name(query):
                print("\t", subreddit)
        except:
            print("Subreddit not found!")
            time.sleep(1)
            self.main()
        choice = gp("\nEnter [Y] if you want to open any of the above subreddits.")
        if choice.lower() == "y":
            subreddit = Subreddit(input("Enter the name of the subreddit:"), self.scraper)
            subreddit.main()
        else:
            self.main()

    def search_by_topic(self):
        """A function to search for subreddits by topic."""
        query = input("Enter the topic of the subreddit you want to search:")
        print("Search results:")
        try:
            for subreddit in self.subreddits.search_by_topic(query):
                print("\t", subreddit)
        except:
            print("Subreddit not found!")
            time.sleep(1)
            self.main()
        choice = gp(
            "\nEnter [Y] if you want to open any of the above subreddits.\n"
        )
        if choice.lower() == "y":
            subreddit = Subreddit(input("Enter the name of the subreddit:"), self.scraper)
            subreddit.main()
        else:
            self.main()

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
            self.new_subreddit()
        elif choice.lower() == "p":
            self.popular_subreddits()
        elif choice.lower() == "s":
            self.search()
        elif choice.lower() == "b":
            self.search_by_name()
        elif choice.lower() == "t":
            self.search_by_topic()
        elif choice.lower() == "q":
            print("Returning to main menu as requested...")
            print_main()
        else:
            print("Invalid choice entered. Try again...")
            time.sleep(1)
            self.main()


class Subreddit:
    """A class to utilize the reddit.subreddit instance."""
    def __init__(self, subreddit_name, scraper):
        self.scraper = scraper
        try:
            self.subreddit = scraper.reddit.subreddit(subreddit_name)
            print("You are browsing /r/%s" % self.subreddit.fullname)
            clrscr()
        except:
            print("subreddit does not exist. \nReturning to menu in 2 seconds...")
            time.sleep(2)

    def show_posts(self, sort):
        """A function to show 10 submissions from the subreddit."""
        print(
            f"Fetching 10 {sort['txt']} submissions from {self.subreddit.display_name}... \n\n"
        )
        for submission in sort["func"](limit=10):
            print(submission.title)
            print(f"score={submission.score}")
            choice = gp(
                "[y] to open this submission in your "
                + "browser, [q] to go back to menu, or "
                + "any other key to skip to the next post\n"
            ).lower()
            if choice == "y":
                link_handler("https://redd.it/" + submission.id)
                time.sleep(2)
            elif choice == "q":
                break
        self.main()

    def main(self):
        """The main menu for the subreddit class."""
        if not self.subreddit:
            print_main()
            return

        clrscr()
        banner()
        print(f"Welcome to /r/{self.subreddit.display_name}")
        print(f"Id of subreddit: {self.subreddit.id}")
        print(f"No. of subscribers: {self.subreddit.id}")
        if self.subreddit.user_is_banned:
            print("You're banned from this subreddit.")
        if self.subreddit.user_is_moderator:
            print("You're a moderator of this subreddit.")
        if self.subreddit.user_is_subscriber:
            print("You're subscribed to this subreddit.")
        choice = gp(
            "\nWhat do you want to do here?\n"
            + "[h] to display hot submissions.\n"
            + "[n] to display new submissions.\n"
            + "[t] to display top submissions.\n"
            + "[q] to go back to main menu.\n"
        ).lower()
        sort_types = {
            "h": {"txt": "hot", "func": self.subreddit.hot},
            "t": {"txt": "top", "func": self.subreddit.top},
            "n": {"txt": "new", "func": self.subreddit.new},
        }
        if choice in sort_types:
            self.show_posts(sort_types[choice])
        elif choice == "q":
            print("Returning to main menu as requested...")
            print_main()
        else:
            print("Invalid choice entered. Try again...")
            time.sleep(1)
            self.main()


class Inbox:
    """A class to utilize the reddit.inbox instance."""

    def __init__(self, scraper: Scraper):
        self.scraper = scraper
        self.inbox = scraper.reddit.inbox

    def unread(self):
        """A function to output the unread messages of the user."""
        unread = []
        for item in self.inbox.unread():
            unread.append(item)
        if len(unread) == 0:
            print("You have no unread messages.")
            time.sleep(1)
            self.main()
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
            self.inbox.mark_read(mark_read)
            self.main()

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
            self.unread()
        elif choice.lower() == "q":
            print("Returning to main menu as reqested...")
            print_main()
        else:
            print("Invalid choice entered. Try again...")
            time.sleep(1)
            self.main()
