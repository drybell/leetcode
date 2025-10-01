"""
300. Longest Increasing Subsequence
https://leetcode.com/problems/longest-increasing-subsequence/description/

Given an integer array nums, return the length of the longest strictly increasing subsequence.

Example 1:

Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:

Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:

Input: nums = [7,7,7,7,7,7,7]
Output: 1

Constraints:

1 <= nums.length <= 2500
-104 <= nums[i] <= 104

Follow up: Can you come up with an algorithm that runs in O(n log(n)) time complexity?

Strategy: DP

x = length of array
y = length of longest increasing subsequence (length of LIS)

at y == 1, for any array of size x, the length of the LIS is 1
the maximum possible length of the LIS is x

our DP is initialized as M[x, x]

on first attempt, this approach missed a critical requirement
which is that we can skip elements as we traverse the array.

In this case, i believe y should instead be choosing array[y]
element as the base of the subsequence
"""

def debug_dp(x, y, dp):
    print()
    maxylen = max(map(lambda x: len(str(x)), y))
    print(''.rjust(maxylen + 5) + str(x))

    mat = []

    for row in dp:
        elems = []
        for j, e in enumerate(row):
            if j == 0:
                elems.append('0')
            else:
                elems.append(str(e).rjust(len(str(x[j - 1]))))

        mat.append('[' + ', '.join(elems) + ']')

    print('\n'.join(f"{str(i).rjust(maxylen + 1)} {l}" for i, l in zip([''] + y, mat)))

def lis(nums):
    numlen = len(nums)
    n = numlen + 1

    revnums = list(reversed(nums))

    M = [
        [0] * n
        for i in range(n)
    ]

    for i in range(1, n):
        for j in range(1, n):
            if j > (n - i):
                M[i][j] = M[i-1][j]
            elif nums[i - 1] < revnums[j - 1]:
                M[i][j] = M[i][j - 1] + 1
            else:
                M[i][j] = M[i][j-1]

    debug_dp(revnums, nums, M)
    return M[numlen][numlen]

"""
Cheated :(

I was hung on using a 2D DP table to track, and couldn't
figure out (after trying many options) the axes. The solution
is to use a 1D array and use the following criteria for the DP:

    Let dp[i] be the LIS of nums[0..i] which has nums[i] as the
    end element

The other trick is to make sure that when updating the DP on
a valid comparison, we check if the solution at the current
is the same as the previous

[1, 1,1,1,1,1,  1, 1]
[10,9,2,5,3,7,101,18]
        ^

      V V
[1, 1,1,1,1,1,  1, 1]
[10,9,2,5,3,7,101,18]
      ^ ^
10 & 9 are larger than 5, but 2 is not
5 > 2 and 1 == 1

      j i
      V V
[1, 1,1,2,1,1,  1, 1]
[10,9,2,5,3,7,101,18]
      ^ ^
      j   i
      V   V
[1, 1,1,2,1,1,  1, 1]
[10,9,2,5,3,7,101,18]
      ^   ^
      j     i
      V     V
[1, 1,1,2,2,1,  1, 1]
[10,9,2,5,3,7,101,18]
      ^     ^
        j   i
        V   V
[1, 1,1,2,2,2,  1, 1]
[10,9,2,5,3,7,101,18]
        ^   ^
          j i
          V V
[1, 1,1,2,2,3,  1, 1]
[10,9,2,5,3,7,101,18]
          ^ ^
          j i
          V V
[1, 1,1,2,2,3,  1, 1] <- note we didn't update
[10,9,2,5,3,7,101,18]
          ^ ^
"""

def lis(nums):
    n = len(nums)

    M = [
        1 for _ in range(n)
    ]

    for i in range(0, n):
        for j in range(0, i):
            if nums[i] > nums[j] and M[i] == M[j]:
                M[i] = M[j] + 1

    return max(M)

test = [
    lis([10,9,2,5,3,7,101,18])
    , lis([0,1,0,3,2,3])
    , lis([7,7,7,7,7])
    , lis([4,10,4,3,8,9])
    , lis([50,89,12,30,1,2,3,10,4,5,6,20,7,8,9])
    , lis([1,3,6,7,9,4,10,5,6])
]

"""
GRAVEYARD

M = [
        [1 if i == 1 else 0] * n
        for i in range(n)
    ]

            if nums[j - 2] < nums[j - 1]:
                M[i][j] = M[i][j - 1] + 1
            else:
                M[i][j] = max(M[i - 1][j - 1], M[i][j - 1])


    #print('\n'.join(str(l) for l in M))

def lis(nums):
    numlen = len(nums)
    n = numlen + 1

    M = [
        [0] * n
        for i in range(n)
    ]

    for i in range(1, n):
        for j in range(i + 1, n):
            if nums[i - 1] < nums[j - 1]:
                M[i][j] = max(
                    M[i][j - 1] + 1
                    , M[i - 1][j]
                )
            elif nums[i - 1] > nums[j - 1]:
                M[i][j] = max(M[i - 1][j] - 1, 0)

    print()
    print('     ' + str(nums))
    print('\n'.join(f"{str(i).rjust(4)} {l}" for i, l in zip([''] + nums, M)))
    return M[numlen][numlen]

    #print('        ' + str(nums))
    #print('\n'.join(f"{str(i).rjust(4)} {l}" for i, l in zip([''] + nums, M)))
list(range(1, numlen + 1))

def lis(nums):
    numlen = len(nums)
    n = numlen + 1

    revnums = list(reversed(nums))

    M = [
        [0] * n
        for i in range(n)
    ]
    M[1] = [1] * n

    for i in range(2, n):
        for j in range(1, n):
            if j < i:
                M[i][j] = M[i - 1][j]
            elif revnums[i - 1] > revnums[j - 1]:
                M[i][j] = min(
                    M[i][j - 1] + 1, i
                )
            else:
                M[i][j] = max(M[i][j - 1], M[i - 1][j])

    debug_dp(revnums, revnums, M)
    return M[numlen][numlen]

def lisv1(nums):
    numlen = len(nums)
    n = numlen + 1

    revnums = list(reversed(nums))
    presort = sorted(list(set(nums)))
    presortlen = len(presort)
    m = presortlen + 1

    if presortlen == 1:
        return 1

    M = [
        [0] * m
        for i in range(n)
    ]

    for i in range(1, n):
        for j in range(1, m):
            if revnums[i - 1] < presort[j - 1]:
                M[i][j] = max(
                    M[i - 1][j]
                    , M[i][j - 1] + 1
                )
            else:
                M[i][j] = M[i - 1][j]
            #elif presort[i - 1] == nums[j - 1]:
            #    M[i][j] = 0
            #else:
            #    M[i][j] = max(M[i - 1][j], M[i][j - 1])

    print()
    print('        ' + str(presort))
    print('\n'.join(f"{str(i).rjust(4)} {l}" for i, l in zip([''] + revnums, M)))
    return M[numlen][presortlen]


"""
