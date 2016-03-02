"""Twitter/tweet tools."""
import HTMLParser
import re


def normalise(word):
    """Normalise a word for frequency lookups."""
    # Remove anything except a-z.
    word = re.sub(r'[^\w]', '', word)
    return word.lower()


def tidy(tweet):
    """Tidy a tweet."""
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
