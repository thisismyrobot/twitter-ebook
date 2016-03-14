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


def new_tweet(corpus, min_joins=10):
    """Produce a new sentence from a corpus (list of sentences)."""

    # Normalise the corpus and gather some stats.
    normal_map = collections.defaultdict(list)
    normalised_corpus = []
    for sentence in corpus:
        words = sentence.split(' ')
        normalised_sentence = []
        for word in words:
            normalised_word = tools.normalise(word)
            if normalised_word != '':
                normalised_sentence.append(normalised_word)
                normal_map[normalised_word].append(word)

        if len(normalised_sentence) > 0:
            normalised_corpus.append(' '.join(normalised_sentence))

    # Determine the chosen joining word.
    join_values = collections.defaultdict(float)
    for sentence in normalised_corpus:
        for (word, weight) in join_weights(sentence):
            if len(normal_map[word]) < min_joins:
                continue
            corpus_weight = weight / float(len(normal_map[word]))
            join_values[word] += corpus_weight

    join_pool = []
    for (word, weight) in join_values.items():
        join_pool.extend([word] * int(weight))

    joiner = random.choice(join_pool)

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
