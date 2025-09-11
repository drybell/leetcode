"""
Given a string s, return the longest palindromic substring in s.

Example 1:

Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.
Example 2:

Input: s = "cbbd"
Output: "bb"


2: aa
3: aba
4: abba
5: ababa
6: aabbaa

if index != index:index + size_of_expected_palindrome:
    you don't have to check the contents internally

start out by finding palindromes of size 2 (checking neighbors)
then increment size and check endpoints.

0 1 2 3 4 5 6
x_|_______|_x
x b x a x 1 2 3 0 1 2 3 3 2 1 0 3 2 1 c d z a
|                                           |
|                                         |
|                                       |

work backwards, with longest possible palindrome being of size len(s)

a b a b a b a c
|             | <- 1 8 palindrome, since a != c we continue
                                   without checking the rest
|           |   <- 2 7 palindromes
_____________   <---- this one matches endpoints, check if palindrome

  |           |
|         |     <- 3 6 palindromes
  |         |
    |         |


for a str of len N

N   palindrome exists at index 0 : N - 1

N-1 palindrome exists at index 0 : N - 2
                         index 1 : N - 3
                         index n : N - (n + 2)

N-2 palindrome exists at index 0 : N - 3
                         index 1 : N - 4
                         index 2 : N - 5
                         index n : N - (n + 3)

to build the indices, we just need to iterate over the step size
and only count substrings that exist within the string's bounds

"""

def prob(s : str) -> str:
    is_palindrome = lambda x: x == ''.join(l for l in reversed(x))
    if is_palindrome(s):
        return s

    index   = 0
    longest = ''

    while index < len(s):
        tmp = ''
        ctr = 0
        while index + ctr < index + len(longest) + 2 and index + ctr < len(s):
            letter = s[index + ctr]
            tmp += letter
            longest = tmp if is_palindrome(tmp) and len(tmp) > len(longest) else longest
            ctr += 1

        index += 1

    return longest


def prob2(s : str) -> str:
    is_palindrome = lambda x: x == ''.join(l for l in reversed(x))
    if is_palindrome(s):
        return s

    index   = 0

    build_opts = lambda N, n: [
        [i, i + n - 1]
        for i in range(N)
        if i + n - 1 < N
    ]

    slen = len(s)

    # iterate through palindrome sizes largest to smallest
    for pal_size in reversed(range(slen)):
        opts = build_opts(slen, pal_size)
        for opt in opts:
            if s[opt[0]] == s[opt[1]]:
                tmp = s[opt[0]:opt[1] + 1]
                if is_palindrome(tmp):
                    return tmp

def prob3(s : str) -> str:
    is_palindrome = lambda x: x == ''.join(l for l in reversed(x))
    if is_palindrome(s):
        return s

    index   = 0

    build_opts = lambda N, n: [
        [i, i + n - 1]
        for i in range(N)
        if i + n - 1 < N
    ]

    slen = len(s)

    return [
        s[opt[0]:opt[1] + 1]
            for pal_size in reversed(range(slen))
            for opt in build_opts(slen, pal_size)

        if s[opt[0]] == s[opt[1]] and
           is_palindrome(s[opt[0]:opt[1] + 1])
    ][0]

    #for pal_size in reversed(range(slen)):
    #    opts = build_opts(slen, pal_size)
    #    for opt in opts:
    #        if s[opt[0]] == s[opt[1]]:
    #            tmp = s[opt[0]:opt[1] + 1]
    #            if is_palindrome(tmp):
    #                return tmp

