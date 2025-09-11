"""
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


s = "abcfsdfsdfbdezzzzzzzzl"
p = "abc.*bde.*."

abc.*

CHAR CHAR STAR:.

STAR:CHAR

abcfsdfsbf


mississippi
mis*is*ip*.

0 m m  -> T
1 i i  -> T
2 s s* -> lookahead
     -> 3 s s* -> lookahead
             -> 4 i s* -> F (s* counts for 2 characters (index 2, 3))
4 i i  -> T
5 s s* -> lookahead



"""


def prob(s : str, p : str) -> bool:

    class Star:
        def __init__(self, i, prev):
            self.i    = i
            self.prev = prev

        def __str__(self):
            return f"{self.prev}*"

    class Char:
        def __init__(self, i, s):
            self.val = s
            self.i   = i

        def __str__(self):
            return self.val


    class Wild:
        def __init__(self, i):
            self.i = i

        def __str__(self):
            return '.'



    tokens = []

    i = 0

    while i < len(p):
        token = p[i]

        if (i + 1 <= len(p) - 1) and p[i + 1] == '*':
            tokens.append(Star(i, token))
            i += 1

        elif token == '.':
            tokens.append(Wild(i))

        else:
            tokens.append(Char(i, token))

        i += 1


    def match(i, j):
        if i == len(tokens) or j == len(s):
            return i, j

        curr   = tokens[i]
        letter = s[j]

        print(s[:j + 1])
        print(''.join(str(t) for t in tokens[:i + 1]))
        print()
        if isinstance(curr, Wild):
            return match(i + 1, j + 1)
        elif isinstance(curr, Star):
            if curr.prev != '.' and curr.prev != letter:
                return match(i + 1, j)
            elif i + 1 < len(tokens) and j + 1 < len(s):
                return match(i, j + 1)
            else:
                return match(i, j + 1)
        else:
            if curr.val != letter:
                return match(i, j - 1)

            return match(i + 1, j + 1)

        return False

    j = 0
    i = 0

    i, j = match(i, j)

    print(i, j)

    if i == len(tokens) and j < len(s):
        return False

    if j >= len(s) and i >= len(tokens):
        return True

    if isinstance(tokens[i], Star) and i + 1 == len(tokens):
        return True

    return False



def test():
    assert prob('abcd', 'd*') == False
    assert prob('aa', 'a*') == True
    assert prob('aa', 'a') == False
    assert prob('mississippi', 'mis*is*ip*.') == True
    assert prob('aaba', 'ab*a*c*a') == False
    assert prob('aab', 'c*a*b') == True
    assert prob('ab', '.*c') == False
    assert prob('aaa', 'a*a') == True
