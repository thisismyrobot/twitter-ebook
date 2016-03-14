"""eBook engine."""
import json
import os
import twitter

import tools
import brains


def update():
    """Tweet!"""

    with open('history.txt', 'rb') as hf:
        history = json.loads(hf.read())['history']

    tweet = ''
    while True:
        tweet = brains.new_tweet(
            filter(None, map(tools.tidy, tools.sentence_corpus(history)))
        )
        if len(tweet) <= 140:
            break

    return tweet

    # Connect.
    api = twitter.Api(
        os.environ['CONSUMER_KEY'],
        os.environ['CONSUMER_SECRET'],
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_TOKEN_SECRET'],
        cache=None,
    )
    # Post away!
    api.PostUpdate(tweet)

    return tweet


if __name__ == '__main__':
    print update()
