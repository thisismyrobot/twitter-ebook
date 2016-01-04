# Twitter "eBook" fun

More of an excuse to learn about Markov Chains.

Inspired (and heavily based upon): https://github.com/glasnt/ebooks_aas

This one's occaisionally running at [@thisisyourobot](https://twitter/thisisyourrobot)

## Setup

You'll need to set the four tokens in settings.py and the account name to use
for source data.

You'll need a Google App Engine project and a background GAE cron job to hit
the '/' URL.

## Requirements

All the Google App Engine stuff and some third-party libraries:

    pip install -t lib -r requirements.txt

Ref: https://cloud.google.com/appengine/docs/python/tools/libraries27
