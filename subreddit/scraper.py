import os, sys, time, platform
import webbrowser
import prawcore
from praw.models import Message
from contextlib import suppress
from getpass import getpass as gp

#to add the parent directory to the system path.
sys.path.append('.')

import praw

def clrscr():
    if platform.system().lower() == 'linux':
        os.system('clear')
    elif platform.system().lower() == 'windows':
        os.system('cls')

def banner():
	print('''
	██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██████╗██╗     ██╗
	██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝   ██╔════╝██║     ██║
	██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║█████╗██║     ██║     ██║
	██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║╚════╝██║     ██║     ██║
	██║  ██║███████╗██████╔╝██████╔╝██║   ██║      ╚██████╗███████╗██║
	╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚═════╝╚══════╝╚═╝
	''')
	print('''\t\t\t\t\t\t\tby /u/AyamDobhal\n\n\n''')


def quit():
	print('Exiting...')
	os.sys.exit()

def LinkHandler(link):
    if 'ANDROID_DATA' in os.environ:
        os.system('termux-open-url '+link)
    else:
        webbrowser.open_new_tab(link)

def init_subreddit(reddit,subreddit):
    try:    
        subreddit = reddit.subreddit(subreddit)
        print('You are browsing /r/%s'%subreddit.fullname)
        clrscr()
        return subreddit
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)

class Scraper:
    class User:
    
        def __init__(self, user, limit=10):
            self.user = user
            self.blocked = user.blocked()
            self.karma = user.karma()
            self.subreddits = user.subreddits()
            self.contributor_subreddit = user.contributor_subreddit()
            self.preferences = user.preferences()
            self.me = user.me()

        def BlockedUsers(self):
            if len(self.blocked()) == 0:
                    print('You have not blocked any user.')
            else:
                for usr in self.blocked():
                    print('\t'+str(usr))
            gp('Enter any key to go back.')
            Scraper.User.main(self)
            
        def Preferences(self):
            clrscr()
            banner()
            print('Preferences:')
            prefs = []
            for pref, option in self.preferences().items():
                prefs.append([pref,option])
            for i in range(len(prefs)//4):
                print(prefs[i][0],':',prefs[i][1])
            choice = gp('Do you want to see more preferences?[Y for yes, any other key for no]')
            if choice.lower() == 'y':
                for i in range(len(prefs)//4,len(prefs)//2):
                    print(prefs[i][0],':',prefs[i][1])
            choice = gp('Do you want to see more preferences?[Y for yes, any other key for no]')
            if choice.lower() == 'y':
                for i in range(len(prefs)//2,len(prefs)//2+len(prefs)//4):
                    print(prefs[i][0],':',prefs[i][1])
            choice = gp('Do you want to see more preferences?[Y for yes, any other key for no]')
            if choice.lower() == 'y':
                for i in range(len(prefs)//2+len(prefs)//4,-1):
                    print(prefs[i][0],':',prefs[i][1])
            pref_update = gp('Do you want to update any preference?[Y for yes, any other key for no]')
            if pref_update.lower() == 'y':
                print('Redirecting to reddit.com to change preferences...')
                time.sleep(2)
                LinkHandler('https://reddit.com/prefs/')
                Scraper.User.main(self)
            else:
                Scraper.User.main(self)

        def Subscribed(self):
            for subreddit in self.subreddits():
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                pass #insert browse subreddit option here later

        def main(self):
            link_karma_count = 0
            comment_karma_count = 0
            for item in self.karma().values():
                link_karma_count += item['link_karma']
                comment_karma_count += item['comment_karma']
            clrscr()
            banner()
            print('Hello /u/'+str(self.me()))
            print('Karma count --> link karma : %d comment karma : %d\n\n'%(link_karma_count,comment_karma_count))
            choice = gp('''Enter your choice to continue:
[B] to display users you have blocked.
[P] to display account preferences.
[S] to display subreddits you have subscribed to.
[Q] to go return to main menu.''')
            
            if choice.lower() == 'b':
                Scraper.User.BlockedUsers(self)
            elif choice.lower() == 'p':
                Scraper.User.Preferences(self)
            elif choice.lower() == 's':
                Scraper.User.Subscribed(self)
            elif choice.lower() == 'q':
                print('Returning to main menu as requested...')
                time.sleep(1)
            else:
                print('Invalid choice entered. Try again...')
                time.sleep(1)
                Scraper.User.main(self)

    class Subreddits:
        def __init__(self,subreddits):
            self.new = subreddits.new(limit=10)
            self.popular = subreddits.popular(limit=10)
            self.recommended = subreddits.recommended(limit=10)
            self.search = subreddits.search(limit=10)
            self.search_by_name = subreddits.search_by_name(limit=10)
            self.search_by_topic = subreddits.search_by_topic(limit=10)
        
        def NewSubreddits(self):
            print('Newest subreddits are:')
            for subreddit in self.new(limit=10):
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                Scraper.Subreddit.main(init_subreddit(subreddit))
            else:
                Scraper.Subreddits.main(self)

        def PopularSubreddits(self):
            print('Most popular subreddits right now are:')
            for subreddit in self.popular(limit=10):
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                Scraper.Subreddit.main(init_subreddit(subreddit))
            else:
                Scraper.Subreddits.main(self)
        
        def Recommended(self):
            print('Latest subreddit recommendations for you are:')
            for subreddit in self.recommended(limit=10):
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                Scraper.Subreddit.main(init_subreddit(subreddit))
            else:    
                Scraper.Subreddits.main(self)

        def Search(self):
            query = input('Enter the keyword in the name/description of the subreddit you want to find:')
            print('Search results:')
            for subreddit in self.search(query,limit=10):
                print('\t',subreddit)
            choice = gp('\nEnter [Y] if you want to open any of the above subreddits.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit:')
                Scraper.Subreddit.main(init_subreddit(subreddit))
            else:    
                Scraper.Subreddits.main(self)

        def SearchByName(self):
            query = input('Enter the name of the subreddit you want to search for:')
            print('Search results:')
            for subreddit in self.search_by_name(query,limit=10):
                print('\t',subreddit)
            choice = gp('\nEnter [Y] if you want to open any of the above subreddits.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit:')
                Scraper.Subreddit.main(init_subreddit(subreddit))
            else:    
                Scraper.Subreddits.main(self)

        def SearchByTopic(self):
            query = input('Enter the topic of the subreddit you want to search:')
            print('Search results:')
            for subreddit in self.search_by_topic(query,limit=10):
                print('\t',subreddit)
            choice = gp('\nEnter [Y] if you want to open any of the above subreddits.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit:')
                Scraper.Subreddit.main(init_subreddit(subreddit))
            else:
                Scraper.Subreddits.main(self)
            
        def main(self):
            clrscr()
            banner()
            choice = gp('''What do you want to do?
[N] to show new subreddits.
[P] to show popular subreddits.
[R] to show recommended subreddits.
[S] to search for a subreddit by name/description.
[B] to search for a subreddit by name.
[T] to search for a subreddit by topic.
[Q] to return to main menu''')
            if choice.lower() == 'n':
                Scraper.Subreddits.NewSubreddits(self)
            elif choice.lower() == 'p':
                Scraper.Subreddits.PopularSubreddits(self)
            elif choice.lower() == 'r':
                Scraper.Subreddits.Recommended(self)
            elif choice.lower() == 's':
                Scraper.Subreddits.Search(self)
            elif choice.lower() == 'b':
                Scraper.Subreddits.SearchByName(self)
            elif choice.lower() == 't':
                Scraper.Subreddits.SearchByTopic(self)
            elif choice.lower() == 'q':
                print('Returning to main menu as requested...')
                time.sleep(1)
            else:
                print('Invalid choice entered. Try again...')
                time.sleep(1)
                Scraper.Subreddits.main(self)

    class Subreddit:
        def __init__(self, subreddit):
                self.display_name = self.display_name
                self.id = self.id
                self.fullname = self.name
                self.desc = self.public_description
                self.subscribers = self.subscribers
                self.user_is_banned = self.user_is_banned
                self.user_is_moderator = self.user_is_moderator
                self.user_is_subscriber = self.user_is_subscriber
                self.hot = self.hot(limit=10)
                self.top = self.top(limit=10)
                self.new = self.new(limit=10)
                
        def Hot(self):
            print('Fetching 10 hottest submissions from %s... \n\n'%(self.display_name))
            for submission in self.hot():
                print(submission.title)
                print('score=%s'%(submission.score))
                choice = gp('''Do you want to open this submission in your browser?
Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
                if choice.lower() == 'y':
                    LinkHandler('https://reddit.com/r/%s/comments/%s'%(self.display_name,submission.id))
                    time.sleep(2)
                elif choice.lower() == 'q':
                    break
            Scraper.Subreddit.main(self)
        
        def Top(self):
            print('Fetching top 10 submissions from %s... \n\n'%(self.display_name))
            for submission in self.top():
                print(submission.title)
                print('score=%s'%(submission.score))
                choice = gp('''Do you want to open this submission in your browser?
Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
                if choice.lower() == 'y':
                    LinkHandler('https://reddit.com/r/%s/comments/%s'%(self.display_name,submission.id))
                    time.sleep(2)
                elif choice.lower() == 'q':
                    break
            Scraper.Subreddit.main(self)

        def New(self):
            print('Fetching 10 newest submissions from %s... \n\n'%(self.display_name))
            for submission in self.new():
                print(submission.title)
                print('score=%s'%(submission.score))
                choice = gp('''Do you want to open this submission in your browser?
Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
                if choice.lower() == 'y':
                    LinkHandler('https://reddit.com/r/%s/comments/%s'%(self.display_name,submission.id))
                    time.sleep(2)
                elif choice.lower() == 'q':
                    break
            Scraper.Subreddit.main(self)
        
        def main(self):
            clrscr()
            banner()
            print('Welcome to /r/%s'%self.display_name)
            print('id of subreddit:',self.id)
            print('no. of subscribers:\n',self.subscribers)
            if self.user_is_banned:
                print('''You're banned from this subreddit.''')
            if self.user_is_moderator:
                print('''You're a moderator of this subreddit.''')
            if self.user_is_subscriber:
                print('''You're subscribed to this subreddit.''')
            choice = gp('''What do you want to do here?
[H] to display hot submissions.
[N] to display new submissions.
[T] to display top submissions.
[Q] to go back to main menu.''')
            if choice.lower() == 'h':
                Scraper.Subreddit.Hot(self)
            elif choice.lower() == 'n':
                Scraper.Subreddit.New(self)
            elif choice.lower() == 't':
                Scraper.Subreddit.Top(self)
            elif choice.lower() == 'q':
                print('Returning to main menu as requested...')
                time.sleep(1)
            else:
                print('Invalid choice entered. Try again...')
                time.sleep(1)
                Scraper.Subreddit.main(self)
