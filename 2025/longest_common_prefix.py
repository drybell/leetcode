"""
Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"
Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.

Naive:

transpose the list first

["flower","flow","flight"]

[
    "fff"
    , "lll"
    , "ooi"
    , "wwg"
]

however this only works best if the match is in the beginning

["ssssent", "nent", "brent"]
[
    "snb"
    , "ser"
    , "sne"
    , "stn"
]

we need to first identify the size of the smallest word
and use that as our sliding window to generate the transposed lists

["ssssent", "nent", "brent"]

ssssent
----
 ----
  ----
   ----
"""

def longest_common_substring(strs):
    exhaust_list = [
        False
        for i in range(len(strs))
    ]

    def transpose(strings):
        return [
            sublist
            for sublist in
            zip(*(
                list(word)
                for word in strings
            ))
        ]

    def gen_iterator(index, word, windowsize):
        def iterator(size):
            for i in range(size):
                yield word[i:windowsize+i]

            exhaust_list[index] = True

            while True:
                yield word[i:windowsize+i]

        return iterator(len(word) - windowsize + 1)

    smallest_word_len = min(map(len, strs))
    iterators = [
        gen_iterator(i, word, smallest_word_len)
        for i, word in enumerate(strs)
    ]

    def find_longest_chain(substrings):
        sets = [set(s) for s in substrings]

        if all(map(lambda x: len(x) != 1, sets)):
            return ""

        best_chain = ""
        chain = ""

        last_chain_idx = -2

        for i, s in enumerate(sets):
            if len(s) > 1:
                if len(chain) > len(best_chain):
                    best_chain = chain

                chain = ""
            else:
                last_chain_idx = i
                chain += s.pop()

        if len(chain) > len(best_chain):
            return chain

        return best_chain

    def max_by_len(v1, v2):
        if len(v1) >= len(v2):
            return v1
        else:
            return v2

    longest_chain = ""

    while not all(exhaust_list):
        words = [
            next(substring_generator)
            for substring_generator in iterators
        ]

        transposed = transpose(words)
        print(transposed)
        longest_chain = max_by_len(
            longest_chain
            , find_longest_chain(transposed)
        )

    return longest_chain

test = [
    longest_common_substring(["ssssent", "nent", "brent"])
    , longest_common_substring(["flower","flow","flight"])
    , longest_common_substring(["cir", "car"])
]

def longest_common_prefix(strs):
    longest = ""

    for i in range(min(map(len, strs))):
        letter = set([s[i] for s in strs])

        if len(letter) > 1:
            return longest
        else:
            longest += letter.pop()

    return longest

test = [
    longest_common_prefix(["ssssent", "nent", "brent"])
    , longest_common_prefix(["flower","flow","flight"])
    , longest_common_prefix(["cir", "car"])
]

"""
WOOPS!
I did longest common substring instead of prefix...
well this was a better problem to solve anyway

    def find_unbroken_chain_of_ones(lengths):
        chains = []
        chain = 0
        last_one_idx = -2

        for i, length in enumerate(lengths):
            if length == 1:
                last_one_idx = i
                chain += 1
            else:
                if chain > 0 and last_one_idx + 1 != i:
                    chains.append(chain)
                    chain = 0

        if len(chains) == 0 and chain == 0:
            return 0
        elif len(chains) == 0 and chain > 0:
            return chain

        return max(max(chains), chain)


"""
