import math
import re
import os
import praw
import logging
import time
import datetime
from collections import deque
from operator import itemgetter
from urllib.parse import quote_plus



logging.basicConfig(filename="bot.log", level=logging.INFO)

with open('data/checked.txt', 'w') as x, open('data/anti_spam.txt', 'w') as y:
    x.write('1\n2\n3\n')
    y.write('1\n2\n3\n')

class Colour:
    Green, Red, Purple, White, Yellow = '\033[92m', '\033[91m', '\033[95m', '\033[0m', '\033[93m'

# USER VARIABLES
client_id = 'XXXX'
client_secret = 'XXXX'
user_agent = 'Fish for /r/borrow (by /u/impshum)'

lender_whitelist_file = 'data/lender_whitelist.txt'
borrower_blacklist_file = 'data/borrower_blacklist.txt'
users_file = 'data/anti_spam.txt'
checked_file = 'data/checked.txt'

curr = ['£', '€', 'GBP', 'CAD']
usa = ['usa', 'u.s.a', 'us', 'u.s', 'united states']
pres = ['prearranged', 'pre-arranged', 'prenegotiated', 'pre-negotiated']
range_top = 9999
range_bottom = 100


# REPLY TO SUBMISSION
#error_message = 'You got flagged!'
#url_title = quote_plus(submission.title)
#reply_text = error_message.format(url_title)



# DECLARE INSTANCE
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# RUN THE SPAM CHECK PROGRAM
# def nospam():
#    if not whitelisted:
#        os.system('python3 spam_check.py')

# THE STREAMER
submissions = reddit.subreddit('borrow').stream.submissions()
for submission in submissions:
    title = submission.title
    bodytext = submission.selftext
    created = submission.created_utc
    date = datetime.datetime.fromtimestamp(created)
    sid = submission.id
    user = submission.author

    posted = Colour.Purple + '\n' + str(date.strftime('%d %b %Y - %H:%M'))

    hour = created - 60*60
    if created > hour:

        # CHECK IF SUBMISSION HAS ALREADY BEEN PROCCESSED
        with open('data/checked.txt', 'r+') as checked, open('data/anti_spam.txt', 'a') as anti_spam:
            if sid in map(str.strip, checked):
                print(Colour.Green + str(sid), 'already checked')
                done = 1
            else:
                # print(Colour.Green + '\n' + str(sid), 'writing to checked')
                anti_spam.write(str(user) + '\n')
                checked.write(sid + '\n')
                done = 0

        # BEGIN NEW PROCCESSING SUBMISSION
        if not done:

            print(posted)


            # CHECK AGAINST WHITELIST AND BLACKLIST
            with open(lender_whitelist_file, 'r') as lender_whitelist, open(borrower_blacklist_file, 'r') as borrower_blacklist:
                if user in map(str.strip, lender_whitelist):
                    whitelisted = 1
                    print(Colour.White + title)
                    print(Colour.Green + str(user), 'is whitelisted')
                else:
                    whitelisted = 0
                    if user in map(str.strip, borrower_blacklist):
                        print(Colour.White + title)
                        print(Colour.Red + str(user), 'is blacklisted')
                    else:
                        print(Colour.White + title)
                        print(Colour.Yellow + str(user),
                              'is not whitelisted or blacklisted')

            # CHECK TITLES
            if not ('paypal') in title.lower():
                print(Colour.Red + 'Missing PayPal')
            else:
                print(Colour.Green + 'Contains PayPal')

            # CHECK BORROW RANGE
            this = re.findall('(\d[0-9,.]+)', title)
            req = int(this[0].replace(',', ''))


            if int(req) < int(range_bottom):
                print(Colour.Red + 'Less than', range_bottom)
            elif int(req) > int(range_top):
                print(Colour.Red + 'More than', range_top)
            elif range_bottom <= int(req) <= range_top:
                print(Colour.Green + 'Correct range')
            else:
                pass

            if not any(substring in title.lower() for substring in usa):
                print(Colour.Red + 'Missing USA')
            else:
                print(Colour.Green + 'Contains USA')

            if any(substring in title for substring in curr):
                print(Colour.Red + 'Foreign currency')
            else:
                print(Colour.Green + 'Correct currency')

            if any(substring in title.lower() for substring in pres):
                print(Colour.Red + 'Prearrange found in title')
            elif any(substring in title.lower() for substring in pres):
                print(Colour.Red + 'Prearrange found in content')
            else:
                pass


    else:
        print(Colour.Purple + 'Old post')
