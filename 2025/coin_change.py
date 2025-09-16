"""
322. Coin Change

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:

Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:
Input: coins = [2], amount = 3
Output: -1

Example 3:
Input: coins = [1], amount = 0
Output: 0

unbounded knapsack -> can re-choose coins
"""

def fewest_coins(coins, amount):
    amounts       = amount + 1
    denominations = len(coins) + 1

    M = [[float('inf')] * amounts for _ in range(denominations)]

    # let M(i, j)
    #   => fewest number of coins needed up to denomination i
    #      to reach amount j

    # M(i, j)

    for i in range(denominations):
        for j in range(amounts):
            if i == 0:
                M[i][j] = float('inf')
            elif j == 0:
                M[i][j] = 0
            elif coins[i - 1] == j:
                # coin denomination is the amount
                M[i][j] = 1
            elif coins[i - 1] < j:
                # coin denomination is less than amount
                M[i][j] = min(
                    # add 1 coin with the previous solution
                    # of amount - coin
                    # stays in same row since the number of coins
                    # did not change
                    1 + M[i][j - coins[i - 1]]
                    , M[i - 1][j]
                )
            else:
                M[i][j] = M[i - 1][j]

    #return M

    res = M[len(coins)][amount]
    if res == float('inf'):
        return -1

    return res


test = [
    fewest_coins([1,2,5], 11)
    , fewest_coins([2], 3)
    , fewest_coins([1], 0)
]
