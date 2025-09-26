"""
120. Triangle
https://leetcode.com/problems/triangle/description/

Given a triangle array, return the minimum path sum from top to bottom.

For each step, you may move to an adjacent number of the row below. More formally, if you are on index i on the current row, you may move to either index i or index i + 1 on the next row.

Example 1:

Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
Output: 11

Explanation: The triangle looks like:
   2
  3 4
 6 5 7
4 1 8 3

The minimum path sum from top to bottom is 2 + 3 + 5 + 1 = 11 (underlined above).

Example 2:

Input: triangle = [[-10]]
Output: -10

Constraints:

1 <= triangle.length <= 200
triangle[0].length == 1
triangle[i].length == triangle[i - 1].length + 1
-104 <= triangle[i][j] <= 104

Follow up: Could you do this using only O(n) extra space, where n is the total number of rows in the triangle?
"""

GLOBAL_MAX = 10**4 + 1

def argmin(l, currsum):
    currmin = GLOBAL_MAX
    i = -1

    for idx, val in enumerate(l):
        if val + currsum < currmin:
            currmin = val + currsum
            i = idx

    return i

def min_totalv1(triangle):
    if len(triangle) == 1:
        return sum(triangle[0])

    cache = []
    n = len(triangle)

    def traverse(i, j, tmp):
        if i == n:
            cache.append(tmp)
            return True

        allowed = [
            j, (j + 1)
        ]

        if (min_idx := argmin(triangle[i], tmp)) not in allowed:
            return

        res = traverse(
            i + 1
            , min_idx
            , tmp + triangle[i][min_idx]
        )

        if not res:
            newj = allowed[allowed.index(min_idx)] ^ 1
            return traverse(
                i + 1
                , newj
                , tmp + triangle[i][newj]
            )

        return True

    traverse(1, 0, triangle[0][0])
    return cache[0]

"""
Key Insight:

we take the sum of the left and right and see
which is smaller and choose that side

            2
        3       4
    6       5       9
4       4       8       0

            2
        3       4
        l       r

lsum = 2 + 3 = 5
rsum = 2 + 4 = 6

lsum < rsum so choose left

    3       4
6       5       9
l1      r1
       l2      r2

l1sum = 2 + 3 + 6 = 11
r1sum = 2 + 3 + 5 = 10

l2sum = 2 + 4 + 5 = 11
r2sum = 2 + 4 + 9 = 15

r1sum < l1sum == l2sum < r2sum
we choose right (and don't backtrack)

    6       5       9
4       4       8       0
l1      r1
       l2      r2
               l3      r3

l1sum = 11 + 4 = 15
r1sum = 11 + 4 = 15

l2sum = 10 + 4 = 14
r2sum = 10 + 8 = 18

l3sum = 15 + 8 = 23
r3sum = 15 + 0 = 15

l2sum is best, and since we chose correctly
previously we don't need to backtrack
"""

import heapq

def argmin_gen(l):
    heap = [
        (val, i)
        for i, val in enumerate(l)
    ]

    heapq.heapify(heap)

    while heap:
        yield heapq.heappop(heap)

def argmin(l, generator=True):
    if generator:
        return argmin_gen(l)

    currmin = GLOBAL_MAX
    i = -1

    for idx, val in enumerate(l):
        if val < currmin:
            currmin = val
            i = idx

    return i

def arg_best_sum(t1, t2, generator=True):
    sums = []

    for i, v1 in enumerate(t1):
        sums.extend([
              v1 + t2[i]
            , v1 + t2[i + 1]
        ])

    return argmin(sums, generator=generator)

def brute_force(triangle, method='list'):
    opts = []
    def traverse_sum(i, j, prev):
        if i == len(triangle) - 1:
            opts.append(
                prev + triangle[i][j]
            )
            return

        traverse_sum(i + 1, j, prev + triangle[i][j])
        traverse_sum(i + 1, j + 1, prev + triangle[i][j])

    def traverse_list(i, j, prev):
        if i == len(triangle) - 1:
            opts.append([
                *prev, triangle[i][j]
            ])
            return

        traverse_list(i + 1, j, [*prev, triangle[i][j]])
        traverse_list(i + 1, j + 1, [*prev, triangle[i][j]])

    if method == 'list':
        traverse_list(0, 0, [])
    else:
        traverse_sum(0, 0, 0)
    return opts

def min_totalv2(triangle):

    if len(triangle) == 1:
        return sum(triangle[0])
    if len(triangle) == 2:
        return sum(triangle[0]) + min(triangle[1])

    print()
    print(triangle)
    idxs = []

    for i, (t1, t2) in enumerate(zip(triangle, triangle[1::])):
        bestsums = arg_best_sum(t1, t2)
        _, idx = next(bestsums)

        print('s', i, idxs)
        while idxs and (idx // 2) >= idxs[-1] + 2:
            diff = (idx // 2) - idxs[-1]
            start = len(idxs) - diff

            if start == 0:
                start = 1

            end   = len(idxs)
            check_idxs = list(range(idxs[start] + 1, end))

            print(diff, start, end, check_idxs)
            print([triangle[start + j][idx] for j, idx in enumerate(check_idxs)])

            if sum(
                triangle[start + j][idx]
                for j, idx in enumerate(check_idxs)
            ) < sum(
                triangle[start + j][idx]
                for j, idx in enumerate(idxs[start:])
            ):
                idxs[start:] = check_idxs

            _, idx = next(bestsums)

        idxs.append(idx // 2)

        if i + 1 == len(triangle) - 1:
            idxs.append(
                idx
                if idx % 2 == 1 and idx < len(triangle[i + 1])
                else max(min(idx - 1, len(triangle[i + 1]) - 1), 0)
            )

    return idxs
    return sum(triangle[i][idx] for i, idx in enumerate(idxs))

cache = {}

def walk_to_idx(row, idx, triangle):
    s = 0
    curr = 0

    print(f'walk to {row} {idx}')
    def walk(i, j, tmp):
        tmp += triangle[i][j]
        print(i, j, tmp)

        if i == row:
            return tmp if j == idx else False

        res = walk(i + 1, j, tmp)

        if j < idx:
            if (forward := walk(i + 1, j + 1, tmp)) < res:
                return forward

        return res

    s = walk(0, 0, 0)
    
    print(s)
    return s

def min_totalv3(triangle):
    if len(triangle) == 1:
        return sum(triangle[0])
    if len(triangle) == 2:
        return sum(triangle[0]) + min(triangle[1])

    print()
    print(triangle)
    curr_index = 0
    currsum = triangle[0][0]
    idxs = []

    bestsums = [
        arg_best_sum(t1, t2)
        for (t1, t2) in zip(triangle, triangle[1::])
    ]

    ctr = 0
    while ctr < len(bestsums):
        for weight, row_idx in bestsums[ctr]:
            idx = min(row_idx // 2 + row_idx % 2, ctr + 1)
            print(row_idx, idx)

            if idx in (curr_index, curr_index + 1):
                curr_index = idx
                currsum += triangle[ctr + 1][idx]
                idxs.append(idx)
                break
            elif idx > curr_index:
                walk = walk_to_idx(
                    ctr + 1, idx, triangle
                )
                print(ctr, idx, walk, currsum)
                if walk < currsum:
                    idxs.append(idx)
                    currsum = walk
                    curr_index = idx
                    break

        ctr += 1

    return currsum, idxs

def min_total_dp_attempt(triangle):
    """
    I give up and cheat
    """
    n = len(triangle)
    if n == 1:
        return sum(triangle[0])
    if n == 2:
        return sum(triangle[0]) + min(triangle[1])

    idxs = []
    print()
    print(triangle)

    M = [GLOBAL_MAX for _ in range(n)]
    M[0] = triangle[0][0]

    for i in range(1, n):
        for j in range(0, i, 2):
            cv = M[i - 1] + triangle[i][j]
            nv = M[i - 1] + triangle[i][j + 1]

            M[i] = min(
                nv, cv
            )

            print(M)

    return M[n - 1]

def min_total(triangle):
    """
    Bottom up In-Place DP, cheated
    """
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(i + 1):
            currval = triangle[i + 1][j]
            nextval = triangle[i + 1][j + 1]
            triangle[i][j] = triangle[i][j] + min(currval, nextval)
            print(triangle[i])

    return triangle[0][0]




test = [
    min_total([[2],[3,4],[6,5,7],[4,1,8,3]])
    , min_total([[-1],[2,3],[1,-1,-3]])
    , min_total([[2],[3,4],[6,5,9],[4,4,8,0]])
    , min_total([[-1],[3,2],[-3,1,-1]])
    , min_total([[1],[-5,-2],[3,6,1],[-1,2,4,-3]])
    , min_total([[-7],[-2,1],[-5,-5,9],[-4,-5,4,4],[-6,-6,2,-1,-5],[3,7,8,-3,7,-9],[-9,-1,-9,6,9,0,7],[-7,0,-6,-8,7,1,-4,9],[-3,2,-6,-9,-7,-6,-9,4,0],[-8,-6,-3,-9,-2,-6,7,-5,0,7],[-9,-1,-2,4,-2,4,4,-1,2,-5,5],[1,1,-6,1,-2,-4,4,-2,6,-6,0,6],[-3,-3,-6,-2,-6,-2,7,-9,-5,-7,-5,5,1]])
]
