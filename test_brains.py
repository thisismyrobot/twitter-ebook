"""Tests of the 'brains' of the operation."""
import brains


def test_join_weights():
    """Words in a sentence get weights attached for joins."""

    tweet = 'Hello, how\'re you going this fine day'

    assert brains.join_weights(tweet) == [
        ('Hello,', 0),
        ('how\'re', 6),
        ('you', 6),
        ('going', 15),
        ('this', 8),
        ('fine', 4),
        ('day', 0),
    ]


def test_normalise_corpus():
    """Test we can normalise a corpus."""
    corpus = [
        'Hello, how\'re you?',
        'I\'m good, thanks.',
        'Good.',
        'beer',
        'Gone fishing?',
    ]

    normalised, norm_map = brains.normalise_corpus(corpus)

    assert normalised == [
        'hello howre you',
        'im good thanks',
        'good',
        'beer',
        'gone fishing',
    ]

    assert norm_map == {
        'beer': ['beer'],
        'fishing': ['fishing?'],
        'gone': ['Gone'],
        'good': ['good,', 'Good.'],
        'hello': ['Hello,'],
        'howre': ['how\'re'],
        'im': ['I\'m'],
        'thanks': ['thanks.'],
        'you': ['you?'],
    }
