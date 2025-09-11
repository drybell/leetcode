"""
Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

'.' Matches any single character.
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
"""

"""
Thoughts

we need to break the problem down into two parts:
    1. tokenizing the pattern string
    2. applying the tokenized pattern on the input

The result of 2 will be a boolean, resulting in the
pattern matching the string or not

Tokenization:
    * traverse the pattern string, and mark any special characters
        - dot      (.)
        - asterisk (*)
    * the asterisk will need to be "bound" to a previous token

Application:

once we have the tokenized pattern, we iterate through the pattern
and traverse the string at the same time by inspecting the current
pattern and what is available in the string

Current Pattern => "a"
Current Token   => "a"
Result          => True

Current Pattern => "."
Current Token   => "b"
Result          => True

Current Pattern => "a*"
Current Token   => "b"
Result          => True


is_match('aaaaabdceaaabb', '.*d.e.*')

first iteration
    .* consumes entire string

OR
first iteration
    .* consumes up to next token d

aaaaabdceaaabb
      ^

is_match("mississippi", "mis*is*p*.")


.*d.e.*
^
push Token('.')

.*d.e.*
 ^
pop Token('.')
push Token('*', '.')

.*d.e.*
  ^
push Token('d')
set previous Token('*', '.', Token('d'))

.*d.e.*
     ^

"""

class Token:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev  = prev
        self.next  = next

    def __repr__(self):
        vals = filter(lambda x: x is not None, [self.value, self.prev, self.next])
        return f"Token({', '.join([str(s) for s in vals])})"

def tokenize(pattern):
    tokens = []
    dotstar = None
    dotidx  = 0
    tokenidx = 0

    for i, token in enumerate(pattern):
        match token:
            case '*':
                prev = tokens.pop(-1)
                tmp = Token(token, prev=prev.value)

                tokens.append(tmp)

                if token_idx - 1 >= 0 and tokens[token_idx - 1].next is not None:
                    tokens[token_idx - 1].next = tmp

                dotstar = prev
                dotidx = i
            case _:
                tmp = Token(token)
                if dotstar is not None:
                    if dotidx + 1 == i:
                        tokens[-1].next = tmp

                    dotstar = None

                tokens.append(tmp)

        token_idx = len(tokens) - 1

        print(tokens)

    print('\n'.join([str(t) for t in tokens]))
    print()

    return tokens

def apply(string, tokens):
    TERMINATOR = 10000
    iters = 0

    token_idx  = 0
    string_idx = 0

    print(string, tokens)

    while (
        string_idx < len(string)
            and token_idx < len(tokens)
            and iters < TERMINATOR
    ):
        curr  = string[string_idx]
        token = tokens[token_idx]

        passed_token = False

        print(curr, token)

        if token.prev is not None:
            if token.next is not None:
                if token.next.next is not None:
                    if token.next.prev == curr or token.next.prev == '.':
                        print(f"1 -> {token.next.prev} == {curr}")
                        passed_token=True
                    elif token.next.next.value == curr:
                        print(f"2 -> {token.next.next} == {curr}")
                        token_idx += 1
                    elif (
                        token.prev != curr
                            and token.next.prev != curr
                            and (
                                token.next.next.value == '.'
                                    or token.next.next.value == curr
                            )
                    ):
                        print(f"3 -> {token.next.next.value} == {curr}")
                        token_idx += 2
                else:
                    if (
                        token.next.value == curr
                        or token.next.value == '.'
                    ) and token.prev != curr:
                        print(f"4 -> {token.next.value} == {curr}")
                        token_idx += 2
                    elif (
                        token.next.value == curr
                        or token.next.value == '.'
                    ) and token.prev == curr:
                        if string_idx + 1 == len(string):
                            print(f"5 -> string capped")
                            token_idx += 2
                        elif (
                            string[string_idx + 1] != token.prev
                            and string[string_idx + 1] != token.next.value
                            and token.next.value != '.'
                        ):
                            print(f"6 -> {token} == {string[string_idx + 1]}")
                            return False
            else:
                if token.prev != curr and token.prev != '.':
                    passed_token = True
        elif token.value == '.':
            passed_token = True
        else:
            if curr == token.value:
                passed_token = True
            else:
                return False

        print(passed_token, token_idx)

        if passed_token:
            token_idx += 1

        string_idx += 1
        iters += 1

    print()
    if token.prev is not None and token.next is None and token_idx + 1 == len(tokens):
        token_idx += 1

    return (
        token_idx == len(tokens)
        and string_idx == len(string)
    )

def is_match(string, pattern):
    tokens = tokenize(pattern)
    return apply(string, tokens)


tests = [
    is_match('aab', 'c*a*b') # True
    , is_match('aaa', 'a*a') # True
    , is_match('aaa', 'ab*a*c*a') # True
    , is_match('abcd', 'd*') # False
    , is_match('bbbbbbc', 'b*c') # True
    , is_match('aaaaabdce', '.*d.e') # True
    , is_match("mississippi", "mis*is*p*.") # False
    , is_match("mississippi", "mis*is*ip*.") # True
]
