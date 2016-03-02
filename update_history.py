"""Update history.txt from a user's tweets."""
import json
import operator
import os
import twitter

import tools


if __name__ == '__main__':
    # Connect.
    api = twitter.Api(
        os.environ['CONSUMER_KEY'],
        os.environ['CONSUMER_SECRET'],
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_TOKEN_SECRET'],
        cache=None,
    )

    history = []
    max_id = None
    while True:
        page = api.GetUserTimeline(
            screen_name=os.environ['SOURCE_ACCOUNT'], max_id=max_id, count=200,
            include_rts=False, trim_user=True, exclude_replies=True
        )

        # Filter out some inline RT's
        page = filter(lambda tweet: 'RT' not in tweet.text, page)

        # Indicates no more history
        if len(page) == 0:
            break

        max_id = page[-1].id
        history.extend(map(tools.tidy, map(operator.attrgetter('text'), page)))

    # Remove duplicates and empty (after tidying) tweets
    history = filter(None, list(set(history)))

    with open('history.txt', 'wb') as hf:
        hf.write(json.dumps({'history': history}, indent=2, sort_keys=True))
