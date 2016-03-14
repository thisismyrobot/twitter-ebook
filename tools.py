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
    # Ensure it's unicode
    tweet = unicode(tweet)

    # Convert HTML characters to unicode.
    tweet = HTMLParser.HTMLParser().unescape(tweet)

    # Remove unicode characters - original or from HTML.
    tweet = tweet.encode('ascii', 'ignore')

    # Strip basic characters
    tweet = re.sub(r'[*"()\n\r\t]', '', tweet)

    # Filter certain words
    tweet = ' '.join([word
                      for word
                      in tweet.split(' ')
                      if not(word.startswith('http')
                             or word.startswith('#')
                             or word.startswith('.@')
                             or word.startswith('@')
                             or normalise(word) == '')])

    # Remaining characters to strip
    tweet = re.sub(r'[#@]', '', tweet)

    # Re-apply uniform spacing
    return ' '.join(filter(None, map(string.strip, tweet.split(' '))))


def sentences(tweet):
    """Splits a tweet up into one of more sentences."""
    return filter(None, map(string.strip, re.split('[.?!]', tweet)))


def sentence_corpus(corpus):
    """Converts a corpus of tweets to a corpus of sentences."""
    return list(itertools.chain(*map(sentences, corpus)))
