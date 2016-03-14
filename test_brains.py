"""Tests of the 'brains' of the operation."""
import brains


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


def test_bisect():
    """We create the splits using the middle of sentences."""
    corpus = [
        'Every roadtrip needs someone to tell them to slow down in the corners :)',
        'looking forward to F1 tomorrow night - should be super tight at the top!',
    ]

    normalised_sentences = brains.normalise_corpus(corpus)[0]

    starts, ends = brains.bisect(normalised_sentences, min_occurances=1)

    assert starts == {
        'be': [['looking', 'forward', 'to', 'f1', 'tomorrow', 'night', 'should']],
        'night': [['looking', 'forward', 'to', 'f1', 'tomorrow']],
        'should': [['looking', 'forward', 'to', 'f1', 'tomorrow', 'night']],
        'tell': [['every', 'roadtrip', 'needs', 'someone', 'to']],
        'them': [['every', 'roadtrip', 'needs', 'someone', 'to', 'tell']],
        'to': [['every', 'roadtrip', 'needs', 'someone', 'to', 'tell', 'them']],
    }

    assert ends == {
        'be': [['super', 'tight', 'at', 'the', 'top']],
        'night': [['should', 'be', 'super', 'tight', 'at', 'the', 'top']],
        'should': [['be', 'super', 'tight', 'at', 'the', 'top']],
        'tell': [['them', 'to', 'slow', 'down', 'in', 'the', 'corners']],
        'them': [['to', 'slow', 'down', 'in', 'the', 'corners']],
        'to': [['slow', 'down', 'in', 'the', 'corners']],
    }
