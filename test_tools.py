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
