"""Tweet fabrication engine."""
import collections
import random
import re

import tools


def normalise_corpus(corpus):
    """Normalise the corpus, returning it a normals map.

    Normals map maps normalised word to all the different originals.
    """
    normals_map = collections.defaultdict(list)
    normalised_corpus = []
    for sentence in corpus:
        words = sentence.split(' ')
        normalised_sentence = []
        for word in words:
            normalised_word = tools.normalise(word)
            if normalised_word != '':
                normalised_sentence.append(normalised_word)
                normals_map[normalised_word].append(word)

        if len(normalised_sentence) > 0:
            normalised_corpus.append(' '.join(normalised_sentence))

    return normalised_corpus, normals_map


def bisect(sentences, min_length=5, min_occurances=5):
    """Return a list of the second halves of sentences."""
    starts = collections.defaultdict(list)
    ends = collections.defaultdict(list)
    for sentence in sentences:
        words = sentence.split(' ')
        if len(words) < min_length:
            continue
        i = (len(words) // 2)  # + random.randint(-1, 1)
        starts[words[i]].append(words[:i])
        starts[words[i-1]].append(words[:i-1])
        starts[words[i+1]].append(words[:i+1])
        ends[words[i]].append(words[i+1:])
        ends[words[i-1]].append(words[i:])
        ends[words[i+1]].append(words[i+2:])

    for (word, start) in starts.items():
        if len(start) < min_occurances:
            del starts[word]

    for (word, end) in ends.items():
        if len(end) < min_occurances:
            del ends[word]

    return starts, ends


def new_tweet(corpus):
    """Produce a new sentence from a corpus (list of sentences)."""
    normalised_corpus, normal_map = normalise_corpus(corpus)

    starts, ends = bisect(normalised_corpus)

    joiner = random.choice(starts.keys() + ends.keys())

    tweet = random.choice(starts[joiner]) + [joiner] + random.choice(ends[joiner])

    # Denormalise the words
    for i, word in enumerate(tweet):
        tweet[i] = random.choice(normal_map[word])

        # Usually don't denormalise sentence endings.
        if random.random() < 0.8:
            tweet[i] = re.sub('[,.!?:]$', '', tweet[i])

        # Usually remove capitals
        if tweet[i] == tweet[i].capitalize() and random.random() < 0.9:
            tweet[i] = tweet[i].lower()

    # Sort capitals
    for (i, word) in enumerate(tweet):
        if i == 0 or tweet[i-1][-1] in ('.', '?', '!'):
            tweet[i] = word.capitalize()

    tweet = ' '.join(tweet)

    # Tidy the end
    tweet = re.sub(r'[,:;]$', '', tweet)
    tweet = re.sub(r'([^!?.])$', r'\1.', tweet)

    return tweet
