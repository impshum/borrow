import praw
from collections import deque
from operator import itemgetter


class Colour:
    Green, Red, White, Yellow = '\033[92m', '\033[91m', '\033[0m', '\033[93m'

client_id = 'XXXX'
client_secret = 'XXXX'
user_agent = 'Fish for /r/borrow (by /u/impshum)'


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


checked_file = 'data/checked.txt'

# CHECK FOR SPAM
with open(checked_file) as f:
    last = deque(f, 3)

spam1 = itemgetter(0)(last)
spam3 = itemgetter(0, 1, 2)(last)
spam_count = spam3.count(spam1)


if spam_count == 3:
    print(Colour.Yellow + 'Investigating last 3 submissions')

    spams = []
    for spam in spam3:
        spm = spam.replace('\n', '')
        spammy = reddit.submission(id=spm)
        spams.append(spammy.title)

    spam0 = spams[0]

    if all(spam0 == 0 for spam in spams):
        print(Colour.Red + 'SPAM ALERT')
    else:
        print(Colour.Green + 'Not spam')
