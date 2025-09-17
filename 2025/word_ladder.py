"""
127. Word Ladder
https://leetcode.com/problems/word-ladder/description/

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord
Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Example 1:

Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.

Example 2:

Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.

Strategy:

1. Identify if any words are 1 distance apart from the start word
    - hit -> [hot, hat, hzt, ..., cat,]
2. Use that sublist as starting points for transformations along words

hit -> cog
["hot","dot","dog","lot","log","cog"]



"""

import re

def generate_patterns(word):
    for i in range(len(word)):
        letters = list(word)
        letters[i] = '.'
        yield ''.join(letters)

def words_1letter_apart(word, words):
    reverse_words = words[::-1]
    for pattern in generate_patterns(word):
        for i, word in enumerate(reverse_words):
            match = re.match(pattern, word)
            if match is not None:
                yield len(words) - 1 - i
            else:
                continue

def distance_between_words(w1, w2):
    dist = 0
    for i, letter in enumerate(w1):
        if letter != w2[i]:
            dist += 1

    return dist

def words_1letter_apart(word, words):
    reverse_words = words[::-1]
    return [
        len(words) - 1 - i
        for i, check in enumerate(words)
        if distance_between_words(word, check) == 1
    ]

def chain_of_dist_idx(curr, words):
    idxs = []
    for i, word in enumerate(words):
        dist = distance_between_words(curr, word)
        if dist == 1:
            idxs.append(i)

    return idxs

def traverse(idx, words, iters):
    if len(words) <= 1:
        return [*iters, words[0]]

    new = []
    maxlen = 0
    for newidx in chain_of_dist_idx(words[idx], words[idx + 1:]):
        res = traverse(
            newidx, words[newidx + 1:], [*iters, words[0]]
        )

        if len(new) == 0:
            new = res
            maxlen = len(res)
        else:
            if len(res) > maxlen:
                new = res
                maxlen = len(res)

    return new

def ladder_len(begin, end, words):
    if end not in words:
        return 0

    if begin == words[0] and end == words[-1]:
        return len(words) - 1

    start = chain_of_dist_idx(begin, words)

    final = []

    for i in start:
        final.append(
            traverse(i, words[i:words.index(end) + 1], [])
        )

    if len(final) == 0:
        return 0

    return max(
        map(len, final)
    )

test = [
    ladder_len('hit', 'cog', ['hot','dot','dog','lot','log','cog'])
    , ladder_len('handle', 'zaneys', ['boingo','bonnie','banter','bandle','bandie','zandie', 'zandee', 'zaneee', 'zanete', 'zaneye', 'zaneys'])
    , ladder_len('a', 'c', ['a', 'b', 'c'])
]

"""
GRAVEYARD

def traverse_words(idx, words, iters, final):
    # need to get from words[0] -> words[-1] in shortest path
    # requires us to skip over words that chain 1 distance

    iters.append(words[0])

    if len(words) <= 1:
        return iters

    for newidx in chain_of_dist_idx(
        words[idx], words[idx + 1:]
    ):
        res = traverse_words(
            newidx, words[newidx + 1:], [*iters], final
        )

        if words[-1] in res:
            final.append(res)

    return iters


"""
