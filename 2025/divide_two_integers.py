"""
Given two integers dividend and divisor, divide two integers without using multiplication, division, and mod operator.

The integer division should truncate toward zero, which means losing its fractional part. For example, 8.345 would be truncated to 8, and -2.7335 would be truncated to -2.

Return the quotient after dividing dividend by divisor.

Note: Assume we are dealing with an environment that could only store integers within the 32-bit signed integer range: [−231, 231 − 1]. For this problem, if the quotient is strictly greater than 231 - 1, then return 231 - 1, and if the quotient is strictly less than -231, then return -231.

Example 1:

Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = 3.33333.. which is truncated to 3.

Example 2:

Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7/-3 = -2.33333.. which is truncated to -2.
"""

from functools import reduce

def divide(dividend, divisor):
    if dividend == divisor:
        return 1

    if abs(dividend) == abs(divisor):
        return -1

    value = 0
    quotient = 0
    add_minus = False

    if dividend > 0 and divisor < 0:
        add_minus = True
    elif dividend < 0 and divisor > 0:
        add_minus = True

    if dividend < 0:
        dividend = -1 * dividend
    if divisor < 0:
        divisor = -1 * divisor

    if dividend == 0:
        return 0

    if divisor > dividend:
        return 0

    def multiply(a, b):
        return sum([a] * b) # or sum([a for i in range(b)])

    if divisor != 1:
        if len(str(divisor)) > 4:
            values = []
            quotient = 1

            while (new_div := multiply(divisor, quotient)) <= dividend:
                values.append(new_div)
                quotient += 1

            if new_div > dividend:
                quotient -= 1

        else:
            squares = [divisor]
            new_div = divisor

            while (new_div := multiply(new_div, divisor)) <= dividend:
                squares.append(new_div)

            while dividend > divisor:
                last = len(squares) - 1
                while last >= 0:
                    new_div = squares[last]
                    if new_div <= dividend:
                        dividend -= new_div
                        quotient += squares[last - 1] if last > 0 else 1
                    elif new_div > dividend:
                        last -= 1
    else:
        quotient = dividend

    return min(
        max(
            quotient if not add_minus else -quotient
            , -2 ** 31
        )
        , 2 ** 31 - 1
    )

test = [
    divide(10, 3) # 3
    , divide(7, -3) # -2
    , divide(7, -1)
    , divide(2**31, 2)
    , divide(2**31, 3)
]

"""
GRAVEYARD

def square(v, k=1, prev=0):
    if k == 0:
        return prev

    return square(v, k - 1, prev=reduce(lambda x, y: x + y, [prev] * v if prev != 0 else [v] * v))


"""
