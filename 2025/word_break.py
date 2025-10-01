"""
139. Word Break
https://leetcode.com/problems/word-break/description/

Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

Example 1:

Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:

Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
Note that you are allowed to reuse a dictionary word.

Example 3:

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false

Constraints:

1 <= s.length <= 300
1 <= wordDict.length <= 1000
1 <= wordDict[i].length <= 20
s and wordDict[i] consist of only lowercase English letters.
All the strings of wordDict are unique.

Notes:
Gave up on trying to use a DP table and instead just went
with a recursive approach. Naive recursive ended up with a TLE,
but adding a cache dict tracking fails succeeded
"""

def word_break(s, words, cache):
    if (cachehit := cache.get(s)) is not None:
        return cachehit

    wordlen = len(s)

    if wordlen == 0:
        return True

    search = set(map(len, words))

    for idx in search:
        if idx > len(s):
            continue

        substr = s[:idx]

        if substr in words:
            if word_break(s[idx:], words, cache):
                return True
            else:
                cache[s] = False

    cache[s] = False
    return False


def word_break_wrap(s, words):
    cache = {}

    return word_break(s, words, cache)

test = [
    word_break_wrap("leetcode", ["leet", "code"])
    , word_break_wrap("applepenapple", ['apple', 'pen'])
    , word_break_wrap("catsandog", ['cats', 'dog', 'sand', 'and', 'cat'])
    , word_break_wrap("ab", ['a', 'b'])
    , word_break_wrap("bb", ['a', 'b', 'bbb', 'bbbb'])
    , word_break_wrap('abcd', ["a","abc","b","cd"])
    , word_break_wrap('aaaaaaa', ['aaaa', 'aa'])
]

"""
GRAVEYARD:

def word_break(s, words):
    wordlen = len(s)
    dictlen = len(words)

    x = wordlen
    y = dictlen + 1

    M = [
        [0] * x
        for _ in range(y)
    ]
    #splits = []

    for i in range(1, x):
        for j in range(1, x):
            #print(i, j + 1, s[i - 1:j + 1])
            if s[i - 1:j + 1] in words:
                M[i][j] = 1
                #splits.append((i - 1, j + 1))
            else:
                M[i][j] = M[i - 1][j]

    debug_dp(list(range(1, wordlen)), s[:-1], M)
    return bool(M[wordlen - 1][wordlen - 1])

def word_break(s, words):
    wordlen = len(s)
    dictlen = len(words)
    bigword = ''.join(words)
    bigwordlen = len(bigword)

    #x = wordlen + 1
    #y = dictlen + 1

    #if bigwordlen > wordlen:
    #    y = bigwordlen + 1
    #    Y = bigword
    #    x = wordlen + 1
    #    X = s
    #else:
    #    x = bigwordlen + 1
    #    X = bigword
    #    y = wordlen + 1
    #    Y = s

    y = bigwordlen + 1
    Y = bigword
    x = wordlen + 1
    X = s

    M = [
        [0] * y
        for _ in range(x)
    ]
    #splits = []

    for i in range(1, x):
        for j in range(1, y):
            if X[i - 1] == Y[j - 1]:
                M[i][j] = 1

    debug_dp(X, Y, M)
    return bool(M[x - 1][y - 1])

def word_break(s, words):
    wordlen = len(s)
    dictlen = len(words)
    dictwordlens = list(map(len, words))

    y = wordlen + 1
    Y = s

    Ms = [
        [
            [0] * y
            for _ in range(x + 1)
        ]
        for x in dictwordlens
    ]

    for M, X, x in zip(Ms, words, dictwordlens):
        for i in range(1, x + 1):
            for j in range(1, y):
                if X[i - 1] == Y[j - 1]:
                    M[i][j] = 1

        debug_dp(X, Y, M)

    #return bool(M[x - 1][y - 1])

TLE
def word_break(s, words):
    wordlen = len(s)

    if wordlen == 0:
        return True

    search = set(map(len, words))

    for idx in search:
        if idx > len(s):
            continue

        substr = s[:idx]

        if substr in words and word_break(s[idx:], words):
            return True

    return False


"""
