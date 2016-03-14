"""Twitter/tweet tools."""
import HTMLParser
import itertools
import re
import string


def normalise(word):
    """Normalise a word for frequency lookups."""
    # Remove anything except a-z and &.
    word = re.sub(r'[^\w&]', '', word)
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
                              or word.startswith('#')
                              or normalise(word) == '')])
    tweet = HTMLParser.HTMLParser().unescape(tweet)
    tweet = ' '.join(filter(None, map(str.strip, str(tweet).split(' '))))
    return tweet


def sentences(tweet):
    """Splits a tweet up into one of more sentences."""
    return filter(None, map(string.strip, re.split('[.?!]', tweet)))


def sentence_corpus(corpus):
    """Converts a corpus of tweets to a corpus of sentences."""
    return list(itertools.chain(*map(sentences, corpus)))
