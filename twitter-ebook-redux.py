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
    tweet = ' '.join([re.sub(r'[*"@#()\n\r]', '', word)
                      for word
                      in filter(None, map(str.strip, tweet.split(' ')))
                      if not (word.startswith('http')
                              or word.startswith('@')
                              or word.startswith('.@')
                              or normalise(word) == '')])
    tweet = HTMLParser.HTMLParser().unescape(tweet)
    tweet = ' '.join(filter(None, map(str.strip, str(tweet).split(' '))))
    return tweet


def normalise(word):
    """ Normalise a word for frequency lookups.
    """
    # Remove anything except a-z.
    word = re.sub(r'[^\w]', '', word)
    return word.lower()


def new_tweet(corpus):
    """ Produce a sentence from a corpus (list of sentences).
    """
    starters = set()

    freq = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))

    # Process the corpus
    for tweet in corpus:
        words = tidy(tweet).split(' ')
        starters.add(normalise(words[0]))
        for (i, word) in enumerate(words[1:], 1):
            freq[normalise(words[i-1])][normalise(word)] += 1

    start = random.choice(list(starters))

    stack = [(0, [start,])]
    seen = set()

    tweet = None
    while True:

        # Delete all but the highest n weighted items on the stack
        n = 10000
        stack = sorted(stack[-n:])

        new_stack = []

        for (weight, items) in stack:

            last = items[-1]

            for (con, i_weight) in freq[last].items():
                if con in seen:
                    continue

                seen.add(con)

                new_stack.append(
                    (
                        (weight + i_weight) * (random.random() + 0.5),
                        items + [con]
                    )
                )

        # Detect stability
        if new_stack == []:
            tweet = sorted(stack)[-1][1]
            break

        stack = stack + new_stack

        print len(stack)

    tweet[0] = tweet[0].capitalize()

    return '{}.'.format(' '.join(tweet))


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
    #api.PostUpdate(tweet)


if __name__ == '__main__':
    update()
