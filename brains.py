"""Tweet fabrication engine."""
import collections
import random
import re

import tools


def join_weights(sentence):
    """Return how good each word in a sentence is for joins.

    Higher = better.
    """
    weights = []
    words = sentence.split(' ')
    for (i, word) in enumerate(words):
        weight = min(i, len(words) - i - 1) * len(word)
        weights.append((word, weight))
    return weights


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


def join_pool(normalised_corpus, word_count, min_occurances=10):
    """Return a pool of joiners, weighted so the better ones appear more
    often.

    Expects a normalised corpus.
    """
    join_values = collections.defaultdict(float)
    for sentence in normalised_corpus:
        for (word, weight) in join_weights(sentence):
            if word_count[word] < min_occurances:
                continue
            corpus_weight = weight / float(word_count[word])
            join_values[word] += corpus_weight

    join_pool = []
    for (word, weight) in join_values.items():
        join_pool.extend([word] * int(weight))

    return join_pool


def new_tweet(corpus):
    """Produce a new sentence from a corpus (list of sentences)."""

    # Normalise the corpus and create a normalised word map.
    normalised_corpus, normal_map = normalise_corpus(corpus)

    # Work out a count of every word
    word_count = dict([(word, len(normal_map[word]))
                       for word
                       in normal_map.keys()])

    # Create a weighted pool of words to join on.
    pool = join_pool(normalised_corpus, word_count)

    # Determine the chosen joining word.
    joiner = random.choice(pool)

    # Select sentences containing the joining word
    sentence_candidates = []
    for sentence in normalised_corpus:
        if joiner in sentence.split(' ')[1:-1]:
            sentence_candidates.append(sentence)

    sentences = random.sample(sentence_candidates, 2)

    tweet = (
        sentences[0].split(joiner)[0].strip().split(' ') +
        [joiner] +
        sentences[1].split(joiner)[-1].strip().split(' ')
    )

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
