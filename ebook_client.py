""" eBook engine.
"""
from settings import *

import collections
import operator
import random
import re
import twitter


def tidy(tweet):
    """ Tidy a tweet.
    """
    tweet = tweet.encode('ascii', 'ignore')
    tweet = ' '.join([re.sub(r'[*"]', '', word)
                      for word
                      in tweet.split(' ')
                      if not word.startswith('http')])
    tweet = ' '.join(filter(None, tweet.split(' ')))
    return tweet


def normalise(word):
    """ Normalise a word for frequency lookups.
    """
    word = re.sub(r'[^\w]', '', word)
    return word.lower()


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
    history = map(
        tidy,
        map(
            operator.attrgetter('text'),
            api.GetUserTimeline(
                screen_name=SOURCE_ACCOUNT, count=200, include_rts=False,
                trim_user=True, exclude_replies=True
            )
        )
    )

    # Markov it
    starters = [tweet.split(' ')[0]
                for tweet
                in history]

    freq = collections.defaultdict(list)
    for tw in history:
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
#                word = random.choice(' '.join(history).split(' '))

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

    # Post away!
    api.PostUpdate(tweet)


if __name__ == '__main__':
    update()
