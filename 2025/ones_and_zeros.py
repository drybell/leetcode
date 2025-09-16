"""
474. Ones and Zeroes
https://leetcode.com/problems/ones-and-zeroes/description/

You are given an array of binary strings strs and two integers m and n.

Return the size of the largest subset of strs such that there are at most m 0's and n 1's in the subset.

A set x is a subset of a set y if all elements of x are also elements of y.

Example 1:
Input: strs = ["10","0001","111001","1","0"], m = 5, n = 3
Output: 4
Explanation: The largest subset with at most 5 0's and 3 1's is {"10", "0001", "1", "0"}, so the answer is 4.
Other valid but smaller subsets include {"0001", "1"} and {"10", "1", "0"}.
{"111001"} is an invalid subset because it contains 4 1's, greater than the maximum of 3.

Example 2:

Input: strs = ["10","0","1"], m = 1, n = 1
Output: 2
Explanation: The largest subset is {"0", "1"}, so the answer is 2.



"""

import numpy as np

def find_max_form1(strs, zeros, ones):
    strlen = len(strs)
    sizes = strlen + 1
    num_zeros = zeros + 1
    num_ones = ones + 1

    def count_of(s, what):
        return sum([
            1 if letter == str(what) else 0
            for letter in s
        ])

    M = [
        [
            [0] * sizes
            for _ in range(num_zeros)
        ]
        for _ in range(num_ones)
    ]

    for i in range(0, num_ones):
        for j in range(0, num_zeros):
            for k in range(1, sizes):
                current = strs[k - 1]
                zero_cnt = count_of(current, 0)
                one_cnt = count_of(current, 1)

                if (
                    zero_cnt <= j
                    and one_cnt <= i
                ):
                    M[i][j][k] = (
                        max(
                            # adding the current value
                            # with the solution found
                            # without the current value
                            1 + M[i - one_cnt][j - zero_cnt][k - 1]
                            # the solution at the zero/one count
                            # without the current value
                            , M[i][j][k - 1]
                        )
                    )
                else:
                    M[i][j][k] = M[i][j][k - 1]

    return M
    return M[ones][zeros][strlen]

def find_max_form(strs, zeros, ones):
    strlen = len(strs)
    sizes = strlen + 1

    zero_counts = [s.count('0') for s in strs]
    counts  = [
        (cnt, len(s) - cnt) for s, cnt in zip(strs, zero_counts)
    ]

    M = [
        [0] * (ones + 1)
        for _ in range(zeros + 1)
    ]

    for zero, one in counts:
        for i in range(zeros, zero - 1, -1):
            for j in range(ones, one - 1, -1):
                M[i][j] = max(
                    1 + M[i - zero][j - one]
                    , M[i][j]
                )

    return M[zeros][ones]
    return M

test = [
    find_max_form(["10","0001","111001","1","0"], 5, 3)
    , find_max_form(['10', '0', '1'], 1, 1)
    , find_max_form(['00', '000'], 1, 10)
    , find_max_form(["10001110","11000","111110"], 6, 6)
]


"""
Notes:

brute force approach causes TLE

    for i in range(0, zeros + ones + 1):
        for k in range(1, sizes):
            current = strs[k - 1]
            zero_cnt = count_of(current, 0)
            one_cnt = count_of(current, 1)

            if (
                len(current) <= i
                and zero_cnt <= zeros
                and one_cnt <= ones
            ):
                M[i][k] = (
                    max(
                        # adding the current value
                        # with the solution found
                        # without the current value
                        1 + M[i - zero_cnt - one_cnt][k - 1]
                        # the solution at the zero/one count
                        # without the current value
                        , M[i][k - 1]
                    )
                )
            else:
                M[i][k] = M[i][k - 1]

got stuck trying to use sizes, when i shouldve made the
dp table the zeros and ones.

"""
