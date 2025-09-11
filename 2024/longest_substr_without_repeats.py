"""
Given a string s, find the length of the longest
substring without repeating characters.

Example 1:

Input: s = "abcabcbb"
Output: 3

Explanation: The answer is "abc", with the length of 3.
Example 2:

Input: s = "bbbbb"
Output: 1

Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3

Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.
"""

# TODO: this solution is slow, figure out why
# 
# Thoughts:
# Idea is to iterate through string like so:
#
# First Iteration at index 0:
#
# a b c d e a b c a b a
# ^ ^ ^ ^ ^ ^
# |-|-|-|-|-X 
# |
# result -> 6
#
# Problem is where do we iterate after this point:
#
# Second Iteration
#
# a b c d e a b c a b a
#           ^
#           |
#           index = 5
# 
# This looks like a "greedy" implementation as 
# there could be a possibility that the previous substrings
# could have a longer length, but in this scenario this isn't
# the case because the new index is greater than the value of 
# the largest substring.
# 
# So the next step would be to determine where to start the next index
#       
#     index
#   sub |
#   ___ |
# a b c a a b c d e a b c a b a
# _____ |
# result|      
# 
#
# if the length of the substring is less than the length of the
# current largest substring, we can skip wholeheartedly? 
# 
# Doesn't work in the next example, as the substring doesn't 
# contain the offending duplicate char so we need to start at 
# index 1 to find the largest substring
#
#         i 
#   _____ | 
# a n v i a j
#   ^     |
#   |     assumed index
#   next index
#
# maybe instead we don't toss out the previous words and keep them
# 
# ________X
# a n v i a j 
# 
# a n v i a 
# ^ _____ | 
# |       start here
# |
# pop first
# 
# n v i a j 
# 
# 
# a b c a a b c d e a b c a b a
#
# a b c a 
#   b c a a 
#         a b c d e a 
#           b c d e a b
# 
# this is still very slow, i think we have to do a mix
# 
# a b c a a b c d e a b c a b a 
#       | |         |         |
# ______            |         | 
#         _________ |         | 
#                   __________|
#         1         2         3 
# 
# when do we need to backtrack?
# maybe employ a lookahead 
#  


def prob(s : str) -> int:
    index   = 0
    result  = 0
    slen = len(s)
    while index < slen:
        tmp = []
        for j, letter in enumerate(s[index:]):
            check = tmp.append(letter) if letter not in tmp else False
            if check == False:
                break

        tmplen = len(tmp)
        result = tmplen if tmplen > result else result

        if result >= slen - index:
            break

        index += 1

    return result
