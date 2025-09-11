"""
Input: [7, 1, 5, 3, 6, 4]
Output : 7
    buy on day 2 (price = 1)
    sell on day 3 (price = 5)
    buy on day 4 (price = 3)
    sell on day 5 (price = 6)
    total profit = 7

can't place trades on same day
(buy and sell)

"""

"""
thoughts:

7, 1, 5, 3, 6, 4

take diffs of each element pair

i=0: -6     break
i=1:  4, -2 break
i=2: -2     break
i=3:  3, -2 break

sum positive diffs

cases:
    1. max exists in the middle
        - buy min before max
    2. max exists at end
        - buy min before max
    3. max exists at beginning
        - skip, find next max and buy min before max


1.
    12, 5, 11, 13, 6, 3, 10

    i=0: -7       skip
    i=1: 6, 2, -7 skip
    ...


"""

import numpy as np


def optimal_trade(prices):
    print(f"PRICES: {prices}")
    diffs = []

    i = 0
    while i < len(prices):
        j   = 1
        next_price = prices[i]
        while i + j < len(prices):
            next_diff = prices[i + j] - next_price

            if next_diff < 0:
                break

            next_price = prices[i + j]

            diffs.append(next_diff)
            j += 1

        i = i + j

    print(f"DIFFS:  {np.array(diffs)}")
    res = sum(diffs)
    print(f"PROFIT:  {res}\n")
    return res


tests = np.random.randint(0, 20, (20, 10))
results = np.apply_along_axis(optimal_trade, 1, tests)



