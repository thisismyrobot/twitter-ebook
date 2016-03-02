"""eBook engine."""
import collections
import json
import os
import random
import re
import twitter

import history
from tools import normalise, tidy


def new_tweet(corpus):
    """Produce a sentence from a corpus (list of sentences)."""
    starters = set()

    freq = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    normals = collections.defaultdict(list)

    # Process the corpus
    for tweet in corpus:
        words = tidy(tweet).split(' ')
        starters.add(normalise(words[0]))
        normals[normalise(words[0])].append(words[0])
        for (i, word) in enumerate(words[1:], 1):
            freq[normalise(words[i-1])][normalise(word)] += 1
            normals[normalise(word)].append(word)

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

    # Denormalise the words
    for i, word in enumerate(tweet):
        tweet[i] = random.choice(normals[word])

        # Usually don't denormalise sentence endings.
        if random.random() < 0.8:
            tweet[i] = re.sub('[,.!?:]$', '', tweet[i])

        # Usually remove capitals
        if tweet[i] == tweet[i].capitalize() and random.random() < 0.9:
            tweet[i] = tweet[i].lower()

    # Sort capitals
    for (i, word) in enumerate(tweet):
        if i == 0 or tweet[i-1][-1] in ('.', '?', '!'):
            tweet[i] = word.capitalize()

    tweet = ' '.join(tweet)

    # Tidy the end
    tweet = re.sub(r'[,:;]$', '', tweet)
    tweet = re.sub(r'([^!?.])$', r'\1.', tweet)

    return tweet


def update():
    """Tweet!"""
    tweet = new_tweet(json.loads(history.HISTORY)['history'])

    # Connect.
    api = twitter.Api(
        os.environ['CONSUMER_KEY'],
        os.environ['CONSUMER_SECRET'],
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_TOKEN_SECRET'],
        cache=None,
    )

    # Post away!
    #api.PostUpdate(tweet)

    return tweet


if __name__ == '__main__':
    print update()
