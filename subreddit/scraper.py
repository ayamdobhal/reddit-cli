import os, sys, time, platform
import webbrowser
from contextlib import suppress
from getpass import getpass as gp
from login import authenticate

#to add the parent directory to the system path.
sys.path.append('.')

import praw

#initializing the reddit class
reddit = authenticate()

def clrscr():
    '''A function to clear the previous output.'''
    if platform.system().lower() == 'linux':
        os.system('clear')
    elif platform.system().lower() == 'windows':
        os.system('cls')

def banner():
    '''A function to print the banner/logo.'''
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
    '''A function to exit the script.'''
    print('Exiting...')
    os.sys.exit()

def LinkHandler(link):
    '''A function to handle links across operating systems.'''
    if 'ANDROID_DATA' in os.environ:
        os.system('termux-open-url '+link)
    else:
        webbrowser.open_new_tab(link)

def init_subreddit(reddit,subreddit):
    '''A function to initialize the reddit.subreddit instance.'''
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
    '''A class that has subclasses for utilizing methods provided by praw.'''
    class User:
        '''A class to utilize the reddit.user instance.'''
        def __init__(self, user, limit=10):
            self.user = user
            self.blocked = user.blocked()
            self.karma = user.karma()
            self.subreddits = user.subreddits()
            self.contributor_subreddit = user.contributor_subreddit()
            self.preferences = user.preferences()
            self.me = user.me()

        def BlockedUsers(self):
            '''A function to output the usernames of the users blocked by the authenticated user.'''
            if len(self.blocked()) == 0:
                    print('You have not blocked any user.')
            else:
                for usr in self.blocked():
                    print('\t'+str(usr))
            gp('Enter any key to go back.')
            Scraper.User.main(self)
            
        def Preferences(self):
            '''A function to output the preferences of the authenticated user.'''
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
            '''A function to output the subreddits the authenticated user has subscribed to.'''
            for subreddit in self.subreddits():
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit: ')
                Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
            else:
                Scraper.User.main(self)

        def main(self):
            '''The main menu for the user class.'''
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
        '''A class to utilize the reddit.subreddits instance.'''
        def __init__(self,subreddits):
            self.new = subreddits.new(limit=10)
            self.popular = subreddits.popular(limit=10)
            self.recommended = subreddits.recommended(limit=10)
            self.search = subreddits.search(limit=10)
            self.search_by_name = subreddits.search_by_name(limit=10)
            self.search_by_topic = subreddits.search_by_topic(limit=10)
        
        def NewSubreddits(self):
            '''A function to output 10 newest subreddits.'''
            print('Newest subreddits are:')
            for subreddit in self.new(limit=10):
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit:')
                Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
            else:
                Scraper.Subreddits.main(self)

        def PopularSubreddits(self):
            '''A function to output 10 most popular subreddits.'''
            print('Most popular subreddits right now are:')
            for subreddit in self.popular(limit=10):
                print('\t',subreddit)
            choice = gp('\n\nEnter [Y] if you want to open a subreddit.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit: ')
                Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
            else:
                Scraper.Subreddits.main(self)

        def Search(self):
            '''A function to search for subreddits by name/description.'''
            query = input('Enter the keyword in the name/description of the subreddit you want to find:')
            print('Search results:')
            try:
                for subreddit in self.search(query,limit=10):
                    print('\t',subreddit)
            except:
                print('Subreddit not found!')
                time.sleep(1)
                Scraper.Subreddits.main(self)
            choice = gp('\nEnter [Y] if you want to open any of the above subreddits.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit:')
                Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
            else:    
                Scraper.Subreddits.main(self)

        def SearchByName(self):
            '''A function to search for subreddits by name.'''
            query = input('Enter the name of the subreddit you want to search for:')
            print('Search results:')
            try:
                for subreddit in self.search_by_name(query):
                    print('\t',subreddit)
            except:
                print('Subreddit not found!')
                time.sleep(1)
                Scraper.Subreddits.main(self)
            choice = gp('\nEnter [Y] if you want to open any of the above subreddits.')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit:')
                Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
            else:    
                Scraper.Subreddits.main(self)

        def SearchByTopic(self):
            '''A function to search for subreddits by topic.'''
            query = input('Enter the topic of the subreddit you want to search:')
            print('Search results:')
            try:
                for subreddit in self.search_by_topic(query):
                    print('\t',subreddit)
            except:
                print('Subreddit not found!')
                time.sleep(1)
                Scraper.Subreddits.main(self)
            choice = gp('\nEnter [Y] if you want to open any of the above subreddits.\n')
            if choice.lower() == 'y':
                subreddit = input('Enter the name of the subreddit: ')
                Scraper.Subreddit.main(init_subreddit(reddit,subreddit))
            else:
                Scraper.Subreddits.main(self)
            
        def main(self):
            '''The main menu for the subreddits class.'''
            clrscr()
            banner()
            choice = gp('''What do you want to do?
[N] to show new subreddits.
[P] to show popular subreddits.
[S] to search for a subreddit by name/description.
[B] to search for a subreddit by name.
[T] to search for a subreddit by topic.
[Q] to return to main menu\n''')
            if choice.lower() == 'n':
                Scraper.Subreddits.NewSubreddits(self)
            elif choice.lower() == 'p':
                Scraper.Subreddits.PopularSubreddits(self)
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
        '''A class to utilize the reddit.subreddit instance.'''
        def __init__(self):
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
            '''A function to fetch 10 hottest submissions from the subreddit.'''
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
            '''A function to fetch top 10 submissions from the subreddit.'''
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
            '''A function to fetch 10 latest submissions from the subreddit.'''
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
            '''The main menu for the subreddit class.'''
            clrscr()
            banner()
            print('Welcome to /r/%s'%self.display_name)
            print('id of subreddit:',self.id)
            print('no. of subscribers: %s'%self.subscribers)
            if self.user_is_banned:
                print('''You're banned from this subreddit.''')
            if self.user_is_moderator:
                print('''You're a moderator of this subreddit.''')
            if self.user_is_subscriber:
                print('''You're subscribed to this subreddit.''')
            choice = gp('''\nWhat do you want to do here?
[H] to display hot submissions.
[N] to display new submissions.
[T] to display top submissions.
[Q] to go back to main menu.\n''')
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

    class Inbox:
        '''A class to utilize the reddit.inbox instance.'''
        def __init__(self):
            self.mark_read = self.mark_read()
            self.unread = self.unread()
            self.mark_unread = self.mark_unread()

        def MarkRead(self,msg):
            '''A function to mark an inbox message as read.'''
            self.mark_read(msg)

        def Unread(self):
            '''A function to output the unread messages of the user.'''
            unread = []
            for item in self.unread():
                unread.append(item)
            if len(unread) == 0:
                print('You have no unread messages.')
                time.sleep(1)
                Scraper.Inbox.main(self)
            for msg in unread:
                print('Message id: ',str(msg))
                print('Sent by:',msg.author.name)
                print('Subject:',msg.subject)
                print('Body:',msg.body)
                choice = gp('''Enter [Y] if you want to mark this message as read. 
[B] if you want to block the sender.
[D] if you want to delete this message.
Any other key to continue.''')
                if choice.lower() == 'y':
                    MarkRead(self,msg)
                elif choice.lower() == 'b':
                    msg.author.block()
                elif choice.lower() == 'd':
                    msg.delete()
                Scraper.Inbox.main(self)

        def main(self):
            '''The main menu for the inbox class.'''
            clrscr()
            banner()
            print('Welcome to inbox.')
            choice = gp('''Enter your choice.
[U] to view unread messages.
[Q] to quit to main menu.''')
            if choice.lower() == 'u':
                Scraper.Inbox.Unread(self)
            elif choice.lower() == 'q':
                print('Returning to main menu as reqested...')
                time.sleep(1)
            else:
                print('Invalid choice entered. Try again...')
                time.sleep(1)
                Scraper.Inbox.main(self)