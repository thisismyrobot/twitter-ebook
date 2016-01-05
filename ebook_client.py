""" eBook engine.
"""
from settings import *
from textstat.textstat import textstat

import collections
import HTMLParser
import operator
import random
import re
import twitter


def tidy(tweet):
    """ Tidy a tweet.
    """
    tweet = tweet.encode('ascii', 'ignore')
    tweet = ' '.join([re.sub(r'[*"@#]', '', word)
                      for word
                      in tweet.split(' ')
                      if not (word.startswith('http')
                              or word.startswith('@'))])
    tweet = ' '.join(filter(None, tweet.split(' ')))
    return HTMLParser.HTMLParser().unescape(tweet)


def normalise(word):
    """ Normalise a word for frequency lookups.
    """
    word = re.sub(r'[^\w]', '', word)
    return word.lower()


def new_tweet(corpus):
    """ Produce a sentence from a corpus (list of sentences).
    """
    # Markov it
    starters = [tweet.split(' ')[0]
                for tweet
                in corpus]

    freq = collections.defaultdict(list)
    for tw in corpus:
        words = tidy(tw).split(' ')
        for (i, word) in enumerate(words[1:], 1):
            freq[normalise(words[i-1])].append(word)

    tweet = [random.choice(starters).capitalize()]
    while True:

        # Select the next word
        try:
            word = random.choice(freq[normalise(tweet[-1])])
        except IndexError:
            break

        # Capitalise words on the go
        if tweet[-1][-1] in ('.', '?', '!'):
            word = word.capitalize()

        try:

            tweet.append(word)

            # Exit if over chosen tweet length
            assert len(' '.join(tweet)) <= random.randint(100, 139)

        # Indicates we've made a long enough tweet or reached a full stop.
        except AssertionError:
            break

    tweet = ' '.join(tweet)

    # Fix up the ending
    tweet = re.sub(r'[,:]$', '', tweet)
    tweet = re.sub(r'([^!?.()])$', r'\1.', tweet)

    return tweet


def update():
    """ Tweet!
    """
    # Connect.
    api = twitter.Api(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
    )

    # Get history from source account.
    history = []
    max_id = None
    while True:
        page = api.GetUserTimeline(
            screen_name=SOURCE_ACCOUNT, max_id=max_id, count=200,
            include_rts=False, trim_user=True, exclude_replies=True
        )

        # Indicates no more history
        if len(page) == 0:
            break

        max_id = page[-1].id
        history.extend(map(tidy, map(operator.attrgetter('text'), page)))

    efforts = 0
    tweet = ''
    while efforts < 100:
        tweet = new_tweet(history)
        if textstat.gunning_fog(tweet) > 6:

            print tweet

            # Post away!
            api.PostUpdate(tweet)
            break

        efforts += 1



if __name__ == '__main__':
    update()
