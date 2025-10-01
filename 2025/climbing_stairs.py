"""
70. Climbing Stairs
https://leetcode.com/problems/climbing-stairs/description/

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example 1:

Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:

Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

Constraints:

1 <= n <= 45

Strategy: DP
I want to practice a little more DP, trying to focus on
creating the right table and choosing axes.

climb count
v
  0 1 2 3 4 5 6  7 <- number of steps
0 0 0 0 0 0 0 0  0
1 0 1 1 1 1 1 1  1 <- only one way to count with one step per climb
2 0 1 2 3 5 8 13 21
      ^ ^ ^
      (1,1), (2)
        | |
        (2,1), (1,2), (1,1,1)
          |
          (1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (2,2)

Looks like Fibonnaci, will still try to solve fibonnaci as a DP
table
"""

def climb_dp(n):
    if n < 3:
        return n

    size   = n + 1
    climbs = 3

    M = [[0] * size for _ in range(climbs)]
    M[1] = [1] * size
    M[2][1] = 1
    M[2][2] = 2

    for j in range(3, size):
        M[2][j] = M[2][j - 1] + M[2][j - 2]

    return M[2][n]

# TLE
def climb_fib(n):
    if n < 3:
        return n

    return climb_fib(n - 1) + climb_fib(n - 2)

def climb_cheap(n):
    if n < 3:
        return n

    arr = [1,2,3]

    for i in range(3, n):
        arr.append(arr[i - 1] + arr[i - 2])

    return arr[-1]


test = [
    [climb_dp(i), climb_fib(i), climb_cheap(i)]
    for i in range(1, 20)
]
