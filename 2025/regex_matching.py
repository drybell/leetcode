"""
10. Regular Expression Matching
https://leetcode.com/problems/regular-expression-matching/description/

Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

'.' Matches any single character
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).

Example 1:

Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
Example 2:

Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
Example 3:

Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".

Constraints:

1 <= s.length <= 20
1 <= p.length <= 20
s contains only lowercase English letters.
p contains only lowercase English letters, '.', and '*'.
It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.


Notes:

Trying this one out again, utilizing some of the concepts I've
learned and practiced recently. Starting out with a branching
technique, recursing on choosing stars and not choosing stars.
I'm expecting this to TLE but I want to make sure the recursive
structure is sound and I don't miss test cases.

Recursive branching definitely ended in a TLE, failing on cases
where there are a lot of star tokens in the pattern

I think trying some sort of DP/Knapsack could work

I first started with collapsing the patterns by removing
duplicate star tokens from the pattern string to prune the
search tree, this resulted in a successful pass

At some point I should try the DP approach for practice
"""

class Token:
    def __init__(self, letter):
        self.token = letter
        self.star  = False

    def __repr__(self):
        return f"{self.token}{'*' if self.star else ''}"

def is_match(s, p):
    patterns = []

    last = -1

    for pattern in p:
        match pattern:
            case '*':
                patterns[-1].star = True
                if last > 0:
                    prev_token = patterns[last - 1]
                    if (
                        prev_token.star
                        and prev_token.token == patterns[-1].token
                    ):
                        patterns.pop()
                        last -= 1
            case _:
                patterns.append(Token(pattern))
                last += 1

    result = [None]

    def traverse(pat_i, str_i):
        if result[0] is not None:
            return result[0]

        if str_i == len(s):
            if pat_i == len(patterns):
                result[0] = True
                return True

            while pat_i < len(patterns):
                if patterns[pat_i].star:
                    pat_i += 1
                else:
                    return False

            result[0] = True
            return True
        elif pat_i >= len(patterns):
            return False
        elif str_i > len(s):
            return False

        pattern = patterns[pat_i]
        letter  = s[str_i]

        if pattern.token != '.' and letter != pattern.token:
            if pattern.star:
                return traverse(pat_i + 1, str_i)

            return False
        else: # letter == pattern.token
            if pattern.star:
                return [
                    traverse(pat_i + 1, str_i + 1)
                    , traverse(pat_i, str_i + 1)
                    , traverse(pat_i + 1, str_i)
                ]

            return traverse(pat_i + 1, str_i + 1)

    traverse(0, 0)
    return result[0] is not None

test = [
    is_match('aab', 'c*a*b') # True
    , is_match('aaa', 'a*a') # True
    , is_match('aaa', 'ab*a*c*a') # True
    , is_match('abcd', 'd*') # False
    , is_match('bbbbbbc', 'b*c') # True
    , is_match('aaaaabdce', '.*d.e') # True
    , is_match("mississippi", "mis*is*p*.") # False
    , is_match("mississippi", "mis*is*ip*.") # True
    , is_match("aaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*c")
]


"""
GRAVEYARD

def is_match(s, p):
    patterns = []

    for pattern in p:
        match pattern:
            case '*':
                patterns[-1].star = True
            case _:
                patterns.append(Token(pattern))

    result = [None]

    def traverse(pat_i, str_i):
        if result[0] is not None:
            return result[0]

        if str_i == len(s):
            if pat_i == len(patterns):
                result[0] = True
                return True

            while pat_i < len(patterns):
                if patterns[pat_i].star:
                    pat_i += 1
                else:
                    return False

            result[0] = True
            return True
        elif pat_i >= len(patterns):
            return False
        elif str_i > len(s):
            return False

        pattern = patterns[pat_i]
        letter  = s[str_i]

        if pattern.token != '.' and letter != pattern.token:
            if pattern.star:
                return traverse(pat_i + 1, str_i)

            return False
        else: # letter == pattern.token
            if pattern.star:
                return [
                    traverse(pat_i + 1, str_i + 1)
                    , traverse(pat_i, str_i + 1)
                    , traverse(pat_i + 1, str_i)
                ]

            return traverse(pat_i + 1, str_i + 1)

    traverse(0, 0)
    return result[0] is not None


"""
