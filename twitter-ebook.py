""" eBook engine.
"""
from settings import *

import collections
import HTMLParser
import json
import operator
import random
import re
import twitter


def tidy(tweet):
    """ Tidy a tweet.
    """
    tweet = tweet.encode('ascii', 'ignore')
    tweet = ' '.join([re.sub(r'[*"@#:()\n\r]', '', word)
                      for word
                      in filter(None, map(str.strip, tweet.split(' ')))
                      if not (word.startswith('http')
                              or word.startswith('@')
                              or word.startswith('.@')
                              or re.sub(r'[\d\w]', '', word) == word)])
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
    starters = set()

    freq = collections.defaultdict(list)
    for tw in corpus:
        words = tidy(tw).split(' ')
        starters.add(words[0])
        for (i, word) in enumerate(words[1:], 1):

            # Grab any words after full stops, exclamation marks etc as
            # starters.
            if words[i-1][-1] in ('.', '!', '?'):
                starters.add(word)

            # This is the magic! The more a word is appended after another the
            # more likely it will follow it later in our generated sentence.
            freq[normalise(words[i-1])].append(word)

    tweet = [random.choice(list(starters)).capitalize()]

    added = [normalise(tweet[0])]
    while True:

        # Select the next word
        try:
            word = random.choice(freq[normalise(tweet[-1])])
        except IndexError:
            break

        # Don't repeat words close together
        if normalise(word) in added[-5:]:
            break

        added.append(normalise(word))

        # Capitalise words on the go
        if tweet[-1][-1] in ('.', '?', '!'):
            word = word.capitalize()

        try:

            tweet.append(word)

            # Exit if over chosen tweet length
            assert len(' '.join(tweet)) <= random.randint(70, 139)

        # Indicates we've made a long enough tweet or reached a full stop.
        except AssertionError:
            break

    tweet = ' '.join(tweet)

    # Fix up the ending
    tweet = re.sub(r'[,:]$', '', tweet)
    tweet = re.sub(r'([^!?.])$', r'\1.', tweet)

    return tweet


def update(live=False):
    """ Tweet!
    """
    history = []
    if live:

        # Connect.
        api = twitter.Api(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET,
            cache=None,
        )

        # Get history from source account.
        max_id = None
        while True:
            page = api.GetUserTimeline(
                screen_name=SOURCE_ACCOUNT, max_id=max_id, count=200,
                include_rts=False, trim_user=True, exclude_replies=True
            )

            # Filter out some inline RT's
            page = filter(lambda tweet: 'RT' not in tweet.text, page)

            # Indicates no more history
            if len(page) == 0:
                break

            max_id = page[-1].id
            history.extend(map(tidy, map(operator.attrgetter('text'), page)))

        # Remove duplicates and empty (after tidying) tweets
        history = filter(None, list(set(history)))

        with open('history.txt', 'wb') as hf:
            hf.write(json.dumps({'history': history}, indent=2, sort_keys=True))

    else:
        with open('history.txt', 'rb') as hf:
            history = json.loads(hf.read())['history']

    tweet = new_tweet(history)
    print tweet

    # Post away!
    api.PostUpdate(tweet)


if __name__ == '__main__':
    update()
