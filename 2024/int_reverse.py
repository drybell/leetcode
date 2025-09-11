"""
Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers (signed or unsigned).

Example 1:

Input: x = 123
Output: 321
Example 2:

Input: x = -123
Output: -321
Example 3:

Input: x = 120
Output: 21
"""

def prob(x : int) -> int:
    # reverse digit order
    is_negative = x < 0
    tmp = ''.join(reversed(list(str(abs(x)))))
    test = int(tmp)
    if abs(test) > 2147483648:
        return 0

    return -1 * test if is_negative else test
