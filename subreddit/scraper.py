import os, sys, time, platform
import webbrowser
import prawcore
from contextlib import suppress
from getpass import getpass

#to add the parent directory to the system path.
sys.path.append('.')

import praw
import main

def get_hot(reddit):
    main.clrscr()
    main.banner()
    subreddit = input('Enter the name of the subreddit you want to fetch submissions from:')
    try:
        subreddit = reddit.subreddit(subreddit)
        print('\nFetching hot submissions from %s...\n\n'%(subreddit.title))
        submissions = []
        for submission in subreddit.hot(limit=100):
            print(submission.title)
            print('score=%s'%(submission.score))
            choice = getpass('''Do you want to open this submission in your browser?
            Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
            print('\n\n---------------------------------------\n\n')
            if choice.lower() == 'y':
                if 'ANDROID_DATA' in os.environ:
                    os.system('termux-open-url https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                else:
                    webbrowser.open_new_tab('https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                time.sleep(2)
            elif choice.lower() == 'q':
               	break
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)
        
def get_new(reddit):
    main.clrscr()
    main.banner()
    subreddit = input('Enter the name of the subreddit you want to fetch submissions from:')
    try:
        subreddit = reddit.subreddit(subreddit)
        print('\nFetching new submissions from %s...\n\n'%(subreddit.title))
        submissions = []
        for submission in subreddit.new(limit=100):
            print(submission.title)
            print('score=%s'%(submission.score))
            choice = getpass('''Do you want to open this submission in your browser?
            Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
            print('\n\n---------------------------------------\n\n')
            if choice.lower() == 'y':
                if 'ANDROID_DATA' in os.environ:
                    os.system('termux-open-url https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                else:
                    webbrowser.open_new_tab('https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                time.sleep(2)
            elif choice.lower() == 'q':
               	break
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)

def get_controversial(reddit):
    main.clrscr()
    main.banner()
    subreddit = input('Enter the name of the subreddit you want to fetch submissions from:')
    try:
        subreddit = reddit.subreddit(subreddit)
        print('\nFetching controversial submissions from %s...\n\n'%(subreddit.title))
        submissions = []
        for submission in subreddit.controversial(limit=100):
            print(submission.title)
            print('score=%s'%(submission.score))
            choice = getpass('''Do you want to open this submission in your browser?
            Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
            print('\n\n---------------------------------------\n\n')
            if choice.lower() == 'y':
                if 'ANDROID_DATA' in os.environ:
                    os.system('termux-open-url https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                else:
                    webbrowser.open_new_tab('https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                time.sleep(2)
            elif choice.lower() == 'q':
               	break
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)

def get_rising(reddit):
    main.clrscr()
    main.banner()
    subreddit = input('Enter the name of the subreddit you want to fetch submissions from:')
    try:
        subreddit = reddit.subreddit(subreddit)
        print('\nFetching rising submissions from %s...\n\n'%(subreddit.title))
        submissions = []
        for submission in subreddit.rising(limit=100):
            print(submission.title)
            print('score=%s'%(submission.score))
            choice = getpass('''Do you want to open this submission in your browser?
            Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
            print('\n\n---------------------------------------\n\n')
            if choice.lower() == 'y':
                if 'ANDROID_DATA' in os.environ:
                    os.system('termux-open-url https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                else:
                    webbrowser.open_new_tab('https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                time.sleep(2)
            elif choice.lower() == 'q':
               	break
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)

def get_top(reddit):
    main.clrscr()
    main.banner()
    subreddit = input('Enter the name of the subreddit you want to fetch submissions from:')
    try:
        subreddit = reddit.subreddit(subreddit)
        print('\nFetching top submissions from %s...\n\n'%(subreddit.title))
        submissions = []
        for submission in subreddit.top(limit=100):
            print(submission.title)
            print('score=%s'%(submission.score))
            choice = getpass('''Do you want to open this submission in your browser?
            Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
            print('\n\n---------------------------------------\n\n')
            if choice.lower() == 'y':
                if 'ANDROID_DATA' in os.environ:
                    os.system('termux-open-url https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                else:
                    webbrowser.open_new_tab('https://reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
                time.sleep(2)
            elif choice.lower() == 'q':
               	break
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)