"""Tests of the 'tools'."""
import tools


def test_sentences():
    """Tweets can be broken into sentences."""

    tweet = 'Hello, how\'re you? I\'m great. Good.'

    assert tools.sentences(tweet) == [
        'Hello, how\'re you',
        'I\'m great',
        'Good',
    ]


def test_corpus_to_sentences():
    """Converts a corpus of tweets to a corpus of sentences."""
    tweets = [
        'Hello, how\'re you? I\'m great. Good.',
        'beer',
        'Gone fishing?',
    ]

    assert tools.sentence_corpus(tweets) == [
        'Hello, how\'re you',
        'I\'m great',
        'Good',
        'beer',
        'Gone fishing',
    ]


def test_tidy():
    """We remove things from tweets in history."""
    assert tools.tidy(
        u'.@whoever Every  (roadtrip) \r\nneeds &copy;\tsomeone \xa9 "for" corners :-) #blah # tag cc @whoever2 http://t.co/blah :P',
    ) == 'Every roadtrip needs someone for corners tag cc :P'
