"""
62. Unique Paths
https://leetcode.com/problems/unique-paths/description/

There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 109.

Example 1:

Input: m = 3, n = 7
Output: 28

Example 2:

Input: m = 3, n = 2
Output: 3

Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

Strategy: DP
Continuing from "Climbing Stairs", this one seemed pretty simple
to setup.

To be located at square (i, j), we need to have traversed either
the square directly above or the square to the left of the current,
which means that Cost(i, j) = Cost(i - 1, j) + Cost(i, j - 1)
"""

def unique_paths(m, n):
    x = m + 1
    y = n + 1

    M = [[0] * y for _ in range(x)]

    for i in range(1, x):
        for j in range(1, y):
            if j == 1:
                M[i][j] = 1
            else:
                M[i][j] = (
                    M[i - 1][j]   # cost of getting to square above
                    + M[i][j - 1] # cost of getting to square left
                )

    return M[m][n]

test = [
    ((m, n), unique_paths(m, n))
    for m in range(2, 10)
    for n in range(2, 10)
]
