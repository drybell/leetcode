"""
166. Fraction to Recurring Decimal
https://leetcode.com/problems/fraction-to-recurring-decimal/description/

Given two integers representing the numerator and denominator of a fraction, return the fraction in string format.

If the fractional part is repeating, enclose the repeating part in parentheses.

If multiple answers are possible, return any of them.

It is guaranteed that the length of the answer string is less than 104 for all the given inputs.

Example 1:

Input: numerator = 1, denominator = 2
Output: "0.5"

Example 2:

Input: numerator = 2, denominator = 1
Output: "2"

Example 3:

Input: numerator = 4, denominator = 333
Output: "0.(012)"

Constraints:

-231 <= numerator, denominator <= 231 - 1
denominator != 0

Strategy:

Use long division to identify the recurring remainder for repeating decimals

Getting stuck on how to identify the location to place parens on recurring
"""

#from decimal import Decimal, getcontext
#
#getcontext().prec = 100

#def frac_to_dec(numerator, denominator):
#    decimal = Decimal(numerator) / Decimal(denominator)
#    i, d = int(decimal // 1), decimal % 1
#
#    dec_str = str(d)[2:]

from collections import defaultdict

def start_at_zero(): return 0

def frac_to_dec(numerator, denominator):
    minus_sign = ''

    if numerator < 0 and denominator > 0 or numerator > 0 and denominator < 0:
        minus_sign = '-'

    numerator = abs(numerator)
    denominator = abs(denominator)

    numstr = str(numerator)
    denstr = str(denominator)

    k = len(numstr)
    l = len(denstr)

    qs = [0]
    rs = [int(numstr[:l - 1] or 0)]
    Bs = [0]
    ds = [0]

    cache = defaultdict(start_at_zero)
    is_repeating = False
    loop_start = None

    i = 1
    print()

    while True:
        alpha_i = (
            int(numstr[i + l - 2])
            if i + l - 2 < k
            else 0
        )

        d_i = 10 * rs[i - 1] + alpha_i
        r_i = d_i % denominator
        B_i = d_i // denominator
        q_i = 10 * qs[i - 1] + B_i

        qs.append(q_i)
        ds.append(d_i)
        rs.append(r_i)
        Bs.append(B_i)

        cache[d_i] += 1

        print(d_i, r_i, B_i)

        if r_i == 0 and i > (k - l) + 1:
            break

        if cache[d_i] >= 2 and i > (k - l) + 1:
            is_repeating = True

            for idx in range(len(ds) - 2, 0, -1):
                if ds[idx] == d_i:
                    loop_start = idx
                    break

            break

        i += 1

    if k < l:
        Bs.insert(1, '.')
    else:
        Bs.insert(2 + k - l, '.')

    if loop_start is not None:
        if Bs.index('.') != len(Bs) - 2:
            Bs.pop(-1)

        Bs.insert(max(Bs.index('.') + 1, loop_start + 1), '(')

    base_str = ''.join(str(b) for b in Bs)
    integer, _, decimal = base_str.partition('.')

    if decimal == '0':
        return f"{minus_sign}{int(integer)}"
    if loop_start is not None:
        return f"{minus_sign}{int(integer)}.{decimal})"

    return f"{minus_sign}{int(integer)}.{decimal}"


test = [
    frac_to_dec(1, 2)
    , frac_to_dec(2, 1)
    , frac_to_dec(4, 333)
    , frac_to_dec(1, 23)
    , frac_to_dec(5, 3)
    , frac_to_dec(55, 30)
    , frac_to_dec(1, 28)
    , frac_to_dec(100, 2)
    , frac_to_dec(10, 3)
    , frac_to_dec(100, 3)
    , frac_to_dec(22, 7)
    , frac_to_dec(420, 226)
]

"""
GRAVEYARD

            if rs[-2] != rs[-1]:
                if Bs[rs.index(rs[-1])] == Bs[-1]:
                    if rs.index(rs[-1]) == 1:
                        whole_decimal_repeating = True

                    rs.pop(-1)
                    Bs.pop(-1)
                else:
                    loop_start = rs.index(rs[-1])
            else:
                Bs[-1] = f"({Bs[-1]})"

            break


"""
