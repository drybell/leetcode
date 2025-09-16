"""
518. Coin Change II
https://leetcode.com/problems/coin-change-ii/

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.

Example 1:

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

Example 2:

Input: amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.

Example 3:

Input: amount = 10, coins = [10]
Output: 1
"""

import numpy as np

def total_combs(amount, coins):
    if amount == 0: return 1

    amounts = amount + 1
    denominations = len(coins) + 1

    M = [[0] * amounts for _ in range(denominations)]

    for i in range(1, denominations):
        for j in range(1, amounts):
            if coins[i - 1] == j:
                # can only be one coin
                # but we need to add the solution
                # with the previous subset at the current amount
                # and the solution of the current coin at the
                # current denomination
                M[i][j] = 1 + M[i - 1][j] + M[i][coins[i - 1]]
            elif coins[i - 1] < j:
                M[i][j] = (
                    # the previous solution
                    M[i - 1][j]
                    # the solution without the current coin
                    + M[i][j - coins[i - 1]]
                )
            else:
                M[i][j] = M[i - 1][j]

    #return M
    return M[len(coins)][amount]

test = [
    total_combs(5, [1,2,5])
    , total_combs(3, [2])
    , total_combs(500, [1,2,5])
    , total_combs(10, [1,2,5,7])
    , total_combs(500, [2,7,13])
]
