"""
You are given a string s and an array of strings words. All the strings of words are of the same length.

A concatenated string is a string that exactly contains all the strings of any permutation of words concatenated.

For example, if words = ["ab","cd","ef"], then "abcdef", "abefcd", "cdabef", "cdefab", "efabcd", and "efcdab" are all concatenated strings. "acdbef" is not a concatenated string because it is not the concatenation of any permutation of words.
Return an array of the starting indices of all the concatenated substrings in s. You can return the answer in any order.

Example 1:

Input: s = "barfoothefoobarman", words = ["foo","bar"]

Output: [0,9]

Explanation:

The substring starting at 0 is "barfoo". It is the concatenation of ["bar","foo"] which is a permutation of words.
The substring starting at 9 is "foobar". It is the concatenation of ["foo","bar"] which is a permutation of words.

Example 2:

Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]

Output: []

Explanation:

There is no concatenated substring.

Example 3:

Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]

Output: [6,9,12]

Explanation:

The substring starting at 6 is "foobarthe". It is the concatenation of ["foo","bar","the"].
The substring starting at 9 is "barthefoo". It is the concatenation of ["bar","the","foo"].
The substring starting at 12 is "thefoobar". It is the concatenation of ["the","foo","bar"].


Iteration Strategy:

cap = max(words) - 1 (3 - 1)
idxs = []

barfoofoobarthefoobarman
^
ij

barfoofoobarthefoobarman
^ ^
i j

bar in words -> continue at j + 1
words.clone().pop(index of bar)
idxs.append(0)

barfoofoobarthefoobarman
   ^ ^
   i j

bar in words -> continue at j + 1
words.clone().pop(index of bar)

barfoofoobarthefoobarman
      ^ ^
      i j

foo not in words
reset words, clear idxs


"""


def debug_string(s, i, j):
    print(s)
    iloc = '^'.rjust(i + 1, ' ')
    jloc = '^'.rjust(j - i, ' ')
    iloc2 = 'i'.rjust(i + 1, ' ')
    jloc2 = 'j'.rjust(j - i, ' ')
    print(f"{iloc}{jloc}")
    print(f"{iloc2}{jloc2}")
    print()

from functools import reduce

def substr_all_words(s, words):
    def clone(words):
        return [*words]

    def check_and_get(string, words):
        if string not in words:
            return None

        new = clone(words)
        new.pop([
            i for i, s in enumerate(words)
            if s == string
        ][0])

        return new

    def gen_idx_caps(words):
        return [
            i
            for i in sorted(list(set(map(len, words))))
        ]

    def reduce_results(prev, new):
        match new:
            case list():
                return [*prev, *new]
            case int():
                return [*prev, new]
            case _:
                return prev

    caps = gen_idx_caps(words)
    #printcaps)

    max_substring_len = sum(map(len, words))

    def check_result(i, curr, final=None, maxi=None):
        caps = gen_idx_caps(curr)
        results = []

        #printi, curr, final)

        if len(curr) == 0:
            print(f"exit: {final}")
            return [final]

        for cap in caps:
            if (j := i + cap) == len(s) + 1: continue

            substr = s[i:j]
            result = check_and_get(substr, curr)

            #print"INNER")
            debug_string(s, i, j)
            print(i, j, substr, result, curr)

            if result is None:
                continue

            results.append([j, result, final])

        if len(results) == 0:
            return None

        return reduce(
            reduce_results
            , [
                check_result(*res)
                for res in results
            ]
            , []
        )

    final = []

    i = 0

    while i < len(s) - max_substring_len + 1:
        results = []
        for cap in caps:
            if (j := i + cap) == len(s): continue

            substr = s[i:j]

            result = check_and_get(substr, words)
            #print"OUTER")
            debug_string(s, i, j)
            #printsubstr, words, result)

            if result is None:
                continue

            traversal_results = check_result(j, result, i)

            print(f"TRAVERSAL RESULTS: {traversal_results}")
            if traversal_results:
                final.extend(traversal_results)

            #printtraversal_results, i, substr)

        i += 1

    return final

test = [
    substr_all_words("barfoofoobarthefoobarman", ["bar","foo","the"])
    , substr_all_words("wordgoodgoodgoodbestword", ["word","good","best","word"])
    , substr_all_words("barfoothefoobarman", ["foo","bar"])
    , substr_all_words("bartestmefoosonladiesfoodsonladiesthefoobarman", ["son", "ladies", "food"])
    , substr_all_words("wordgoodgoodgoodbestword", ["word","good","best","good"])
    , substr_all_words("lingmindraboofooowingdingbarrwingmonkeypoundcake", ["fooo","barr","wing","ding","wing"])
]

# FINISHED SOLUTION
# MINUS TIME CONSTRAINTS (s = 'a' * 100, words = ['a'] * 150)

def substr_all_words(s, words):
    if ''.join(words) == s:
        return [0]

    if s.startswith(''.join(words)) and len(''.join(words)) > len(s):
        return []

    def clone(words):
        return [*words]

    def check_and_get(string, words):
        if string not in words:
            return None

        new = clone(words)
        new.pop([
            i for i, s in enumerate(words)
            if s == string
        ][0])

        return new

    def gen_idx_caps(words):
        return [
            i
            for i in sorted(list(set(map(len, words))))
        ]

    def reduce_results(prev, new):
        match new:
            case list():
                return [*prev, *new]
            case int():
                return [*prev, new]
            case _:
                return prev

    caps = gen_idx_caps(words)

    max_substring_len = sum(map(len, words))

    def check_result(i, curr, final=None, maxi=None):
        caps = gen_idx_caps(curr)
        results = []

        if len(curr) == 0:
            return [final]

        for cap in caps:
            if (j := i + cap) == len(s) + 1: continue

            substr = s[i:j]
            result = check_and_get(substr, curr)

            if result is None:
                continue

            results.append([j, result, final])

        if len(results) == 0:
            return None

        return reduce(
            reduce_results
            , [
                check_result(*res)
                for res in results
            ]
            , []
        )

    final = []

    i = 0

    while i < len(s) - min(caps):
        results = []
        for cap in caps:
            if (j := i + cap) == len(s): continue

            substr = s[i:j]

            result = check_and_get(substr, words)
            if result is None:
                continue

            traversal_results = check_result(j, result, i)

            if traversal_results:
                final.extend(traversal_results)

        i += 1

    return final


"""
GRAVEYARD

    #results.append(result) # for each result we may need to re-iterate to attempt another checking branch line

    def check_current_set(i):
        curr = clone(words)
        results = []

        while i <= max_substring_len - min(caps) and len(curr) > 0:
            for cap in caps:
                j = i + cap

                if j == len(s):
                    continue

                substr = s[i:j + 1]
                result = check_and_get(substr, curr)

                if result is None:
                    continue

                results.append([j, result])

            for result in results:
                ...
"""
