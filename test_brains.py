"""Tests of the 'brains' of the operation."""
import brains


def test_join_weights():
    """Words in a sentence get weights attached for joins."""

    tweet = 'Hello, how\'re you going this fine day'

    assert brains.join_weights(tweet) == [
        ('hello', 0),
        ('howre', 5),
        ('you', 6),
        ('going', 15),
        ('this', 8),
        ('fine', 4),
        ('day', 0),
    ]
