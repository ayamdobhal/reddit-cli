import os, sys, time
import webbrowser
import prawcore
from contextlib import suppress

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
        for submission in subreddit.hot(limit=10):
            print(submission.title, 'id=%s'%(submission.id))
            print('score=%s'%(submission.score))
            choice = input('''Do you want to open this submission in your browser?
                         Y for yes, Q to go back to menu or any other key to skip to next submission\n''')
            print('--------------------------------------------------------------------------------------------')
            if choice.lower() == 'y':
                webbrowser.open_new_tab('reddit.com/r/%s/comments/%s'%(subreddit,submission.id))
            elif choice.lower() == 'q':
                break
    except:
        print('subreddit does not exist. \nReturning to menu in 2 seconds...')
        time.sleep(2)
        suppress(Exception)
        
    