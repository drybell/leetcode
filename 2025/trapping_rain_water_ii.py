"""
407. Trapping Rain Water II
https://leetcode.com/problems/trapping-rain-water-ii/description

Given an m x n integer matrix heightMap representing the height of each unit cell in a 2D elevation map, return the volume of water it can trap after raining.

Example 1:
Input: heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]
Output: 4
Explanation: After the rain, water is trapped between the blocks.
We have two small ponds 1 and 3 units trapped.
The total volume of water trapped is 4.

Example 2:
Input: heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]
Output: 10

Constraints:

m == heightMap.length
n == heightMap[i].length
1 <= m, n <= 200
0 <= heightMap[i][j] <= 2 * 104

Strategy:

I want to employ something different than my home-baked solution
to the first variant of this problem (double-pointerish tracking local maxima).

I feel like this can be solved by pulling inspiration from gradient
descent. We want to identify local minima areas enclosed by local
maxima (surrounding points higher than the identified minima).

We can omit checking walls and instead check only the innner elems

0 < i & j
i < width  - 1
j < height - 1

        j
        v
    [1, 4, 3, 1, 3, 2]
i > [3, 2, 1, 3, 2, 4] < imax
    [2, 3, 3, 2, 3, 1]
                 ^
                 jmax

I'm going to try a depth-first search with memoization, where we'll
attempt to traverse neighbors that are smaller than an identified
local maxima (or maxima set)

        j
        v
    [1, 4, 3, 1, 3, 2]
i > [3, 2, 1, 3, 2, 4]
    [2, 3, 3, 2, 3, 1]

M[i][j] = 2
neighbors(i, j) = [3, 4, 3, 1]

local maxima = maxheap([4, 3]) or maybe minheap

Goal:     identify if (i, j) is a candidate for traversal
Criteria: What constitutes a "well" candidate (where water can be trapped?)

Initial Hypothesis:

An M[i,j] is considered a "well candidate" if two neighbors are
larger than it. We want to traverse the other smaller or equal
in magnitude neighbors to continue candidacy and track the running
diff between each wc and the smallest max of all neighbors

"""

import numpy as np


def clamp(loc, w, h):
    x, y = loc

    return (
        max(min(x, w - 1), 0)
        , max(min(y, h - 1), 0)
    )

def cardinal_neighbors(M, i, j):
    return np.array([
        clamp((i + 1, j), *M.shape)
        , clamp((i - 1, j), *M.shape)
        , clamp((i, j + 1), *M.shape)
        , clamp((i, j - 1), *M.shape)
    ])

def get_neighbors(M, i, j):
    neighbors = cardinal_neighbors(M, i, j)
    values    = M[*neighbors.T]
    return neighbors, values

def candidate_at_outer_wall(M, i, j):
    if i == 0 or j == 0:
        return True
    if i == M.shape[0] - 1 or j == M.shape[1] - 1:
        return True

    return False

def get_local_maxima(M, current, neighbors, values):
    cmp = values > current

    maxima = np.array([
        [*idx, value]
        for idx, value in zip(neighbors, values)
        if (
            value > current
            or (
                value == current
                and candidate_at_outer_wall(M, *idx)
            )
        )
    ])

    if maxima.shape[0] < 2:
        return None, None

    if maxima.shape[0] == 2:
        print(maxima)
        (i1, i2), (j1, j2) = maxima[:2, :2]
        if abs(i1 - j1) == 2 or abs(i2 - j2) == 2:
            return None, None

    candidates = np.array([
        candidate
        for candidate in neighbors[values <= current]
        if not candidate_at_outer_wall(M, *candidate)
    ])

    if not candidates.shape[0]:
        if cmp.all():
            return maxima[:, 2], candidates

        return None, None

    return maxima[:, 2], candidates

def get_next_well_candidates(M, i, j):
    current   = M[i, j]
    neighbors, values = get_neighbors(M, i, j)
    return get_local_maxima(M, current, neighbors, values)

def spiral_traversal(M):
    N = []

    top    = 0
    bottom = M.shape[0] - 1

    left   = 0
    right  = M.shape[1] - 1

    while top <= bottom and left <= right:
        # left -> right
        for col in range(left, right + 1):
            N.append((top, col))

        top += 1

        # top-right -> bottom-right
        for row in range(top, bottom + 1):
            N.append((row, right))

        right -= 1

        # bottom-right -> bottom-left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                N.append((bottom, col))

            bottom -= 1

        # bottom-left -> top-left
        if left <= right:
            for row in range(bottom, top - 1, -1):
                N.append((row, left))

            left += 1

    return N

def inner_spiral_traversal(M, exclude_walls=True):
    rows, cols = M.shape
    layers = (min(rows, cols) + 1) // 2

    for layer in range(layers - 1, -1 if not exclude_walls else 0, -1):
        top = layer
        bottom = rows - layer - 1
        left = layer
        right = cols - layer - 1

        indices = []

        for j in range(left, right + 1):
            indices.append((top, j))

        for i in range(top + 1, bottom + 1):
            indices.append((i, right))

        if bottom != top:
            for j in range(right - 1, left - 1, -1):
                indices.append((bottom, j))

        if left != right:
            for i in range(bottom - 1, top, -1):
                indices.append((i, left))

        indices = np.array(indices)
        values = M[indices[:, 0], indices[:, 1]]

        yield indices, values

def trap_exploration(heightmap):
    M = np.array(heightmap)
    w, h = M.shape

    wells = np.zeros((w - 2, h - 2)).tolist()
    vals  = np.zeros((w - 2, h - 2)).tolist()

    for i in range(1, w - 1):
        for j in range(1, h - 1):
            #wells[i - 1][j - 1] = get_next_well_candidates(M, i, j)
            maxima, candidates = get_next_well_candidates(M, i, j)
            if maxima is not None:
                print(maxima)
                wells[i - 1][j - 1] = candidates
                vals[i - 1][j - 1] = (
                    min(maxima) - M[i, j]
                )
                M[i, j] = min(maxima)

    return M, wells, vals

def trap(heightmap):
    M = np.array(heightmap)

    height = M.flatten()
    if all(height[i] > height[i+1] for i in range(len(height) - 1)):
        return 0

    if all(height[i] < height[i+1] for i in range(len(height) - 1)):
        return 0

    w, h = M.shape

    rain_volume = [0]
    traversed = []

    def traverse(i, j):
        maxima, candidates = get_next_well_candidates(M, i, j)
        print(maxima, candidates)
        if maxima is not None:
            rain_volume[0] += min(maxima) - M[i, j]
            M[i, j] = min(maxima)
            traversed.append((i, j))

            for candidate in sorted(candidates, key=lambda c: M[*c]):
                traverse(*candidate)

    for idxs, values in inner_spiral_traversal(M):
        for i, j in idxs[np.argsort(-values)]:
            if (i, j) in traversed:
                continue

            traverse(i, j)

    # TODO: the problem is that we're setting too early,
    # and instead need to traverse dfs until we detect the full
    # bounded area of walls that surround the well. then we can
    # select a specific min of maxima to set each node

    return M, rain_volume[0]

test = [
    trap([[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]])
    , trap([[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]])
    , trap([[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1],[3,1,5,2,1,4]])
    , trap([[12,13,1,12],[13,4,13,12],[13,8,10,12],[12,13,12,12],[13,13,13,13]])
    , trap([[2,3,4],[5,6,7],[8,9,10],[11,12,13],[14,15,16]])
    , trap([[5,5,5,1],[5,1,1,5],[5,1,5,5],[5,2,5,8]])
]

"""
GRAVEYARD:

# this one was super close, but we need to slightly adjust
# the implementation to run recursively through dfs and picking
# the smallest neighbors first
def trap(heightmap):
    M = np.array(heightmap)
    w, h = M.shape

    outer_wall_idx = w * 2 + (h - 2) * 2
    rain_volume = 0

    for (i, j) in spiral_traversal(M)[outer_wall_idx:]:
        maxima, candidates = get_next_well_candidates(M, i, j)

        if maxima is not None:
            rain_volume += min(maxima) - M[i, j]
            M[i, j] = min(maxima)

    return rain_volume
"""
