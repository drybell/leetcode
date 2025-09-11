"""
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.

Example 1:

Input: s = "()"
Output: true

Example 2:

Input: s = "()[]{}"
Output: true

Example 3:

Input: s = "(]"
Output: false

Example 4:

Input: s = "([])"
Output: true

Example 5:

Input: s = "([)]"
Output: false

To check for open and closes, just count
each and check for equality.

for nested, need to check for inner close
while there is an open paren

([)]
^
( -> 1

([)]
 ^
( -> 1
[ -> 1

([)]
  ^
( -> 2
[ -> 1

) fails due to ] != [


([)]
^
push (

([)]
 ^
push [

([)]
  ^
pop [


"""

def valid_parens(s):
    closed_map = {
        ')': '('
        , ']': '['
        , '}': '{'
    }

    open_brackets = ['(', '[', '{']

    stack = []

    for letter in s:
        if letter in open_brackets:
            stack.insert(0, letter)
        else:
            if len(stack) == 0:
                return False

            found = stack.pop(0)
            if found != closed_map[letter]:
                return False

    return len(stack) == 0


test = [
    valid_parens("()")
    , valid_parens("()[]{}")
    , valid_parens("(]")
    , valid_parens("(])")
    , valid_parens("([)]")
    , valid_parens("([])")
]
