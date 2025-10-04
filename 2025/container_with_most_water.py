"""
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.


|
|
|
|
|
|
|   |         |
|   |         |   |
|   | |       |   |
|   | |   |   |   |
|   | |   | | |   |
|   | |   | | | | |
|   | | | | | | | |
| | | | | | | | | |
|--------------------

Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
Example 2:

Input: height = [1,1]
Output: 1

naive

current_max = None
buckets = [1,8,6,2,5,4,8,3,7]

[1,8,6,2,5,4,8,3,7]
 ^
None

[1,8,6,2,5,4,8,3,7]
 ^ ^
((1 - 0) * min(1, 8)) = 1

[1,8,6,2,5,4,8,3,7]
 ^   ^
(2 - 0) * min(1, 6) = 2

[1,8,6,2,5,4,8,3,7]
   ^ ^       ^   ^

[1,8,6,2,5,4,8,3,7]
   ^             ^

(8 - 1) * min(8, 7) = 7 * 7 = 49

Identify the largest gap between items on x axis
identify the largest min between items on y axis

maximize (jx - ix)
maximize min(jy, iy)

[1,8,6,2,5,4,8,3]
       ^ ^
       ^   ^
       ^     ^
       ^       ^
     ^   ^
   ^     ^
 ^       ^

sliding_window = len(h)
[1,8,6,2,5,4,8,3]
 ^             ^

sliding_window = len(h) - 1
[1,8,6,2,5,4,8,3]
 ^           ^
[1,8,6,2,5,4,8,3]
   ^           ^

sliding_window = len(h) - 2
[1,8,6,2,5,4,8,3]
 ^         ^
[1,8,6,2,5,4,8,3]
   ^         ^
[1,8,6,2,5,4,8,3]
     ^         ^

at each next iteration, if the max height i

[1,8,6,2,5,4,8,3,7]
         ^ ^

[1,8,6,2,5,4,8,3,7]
     ^     ^

[1,8,6,2,5,4,8,3,7]
   ^         ^

[1,8,6,2,5,4,8,3,7]
 ^           ^

[1,8,6,2,5,4,8,3,7]
   ^           ^

[1,8,6,2,5,4,8,3,7]
   ^             ^

"""

def max_area2(height):
    window_idx = 0
    get_sliding_window = lambda i: len(height) - i

    gety = lambda jx, ix: (height[jx], height[ix])

    get_width  = lambda jx, ix: abs(jx - ix)
    get_height = lambda jy, iy: min(jy, iy)

    get_area = lambda width, height: width * height

    def gen_sliding_window_pairs(idx):
        window = get_sliding_window(idx)

        j = window
        i = 0

        pairs = []

        while j < len(height):
            pairs.append((i, j))
            i += 1
            j += 1

        return pairs

    def get_max_height_of_window(idx):
        window = get_sliding_window(idx)
        return window * max([
            get_height(*gety(i, j))
            for j in range(window, len(height))
            for i in range(idx)
        ])

    tallest = max(height)

    print(f"LARGEST POSSIBLE: {len(height) * max(height)}")

    def area(jx, ix):
        h = get_height(*gety(jx, ix))
        return h, get_area(get_width(jx, ix), h)

    max_area   = 0
    max_height = 0

    for idx in range(1, len(height)):
        curr_width = get_sliding_window(idx)
        print(f"WINDOW SIZE: {curr_width}")

        if curr_width * tallest < max_area:
            return max_area

        for leftx, rightx in gen_sliding_window_pairs(idx):
            curr_height, curr = area(leftx, rightx)
            max_area = max(curr, max_area)
            max_height = max(curr_height, max_height)
            print(f"AREA   -> {curr}, MAX -> {max_area}")
            print(f"HEIGHT -> {curr_height}, MAX -> {max_height}")

        print()

    print()

    return max_area

def max_area(height):
    get_sliding_window = lambda i: len(height) - i

    gety = lambda jx, ix: (height[jx], height[ix])

    get_width  = lambda jx, ix: abs(jx - ix)
    get_height = lambda jy, iy: min(jy, iy)

    get_area = lambda width, height: width * height

    def get_max_height_of_window(idx):
        window = get_sliding_window(idx)
        return window * max([
            get_height(*gety(i, j))
            for i, j in enumerate(range(window, len(height)))
        ])

    tallest = max(height)
    max_area = 0

    for i in range(1, len(height)):
        if get_sliding_window(i) * tallest < max_area:
            return max_area

        max_area = max(max_area, get_max_height_of_window(i))

    return max([
        get_max_height_of_window(i)
        for i in range(1, len(height))
    ])

def max_area3(height):

    best = list(reversed(sorted(height)))

    def is_sorted_descending(lst):
        return all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1))

    if list(reversed(best)) == height:
        x1 = len(height) // 2 - 1
        x2 = len(height) - 1
        h  = min(height[x1], height[x2])
        return (x2 - x1) * h

    if is_sorted_descending(height):
        x1 = 0
        x2 = len(height) // 2
        h  = min(height[x1], height[x2])
        return (x2 - x1) * h

    def get_area(val1, val2):
        if val1 == val2:
            idxs = [
                i for i in range(len(height))
                if height[i] == val1
            ]
            left, right = idxs[0], idxs[-1]
        else:
            left = [
                i for i in range(len(height))
                if height[i] == val1
            ][0]

            right = [
                i for i in range(len(height))
                if height[i] == val2
            ][-1]

        width = 1 if abs(right - left) == 1 else (
            abs(right - left)
            if (
                left != 0 and right != 0
                or left == 0 and right == len(height) - 1
            )
            else abs(right - left) + 1
        )
        return width * min(val2, val1)

    best_area = 0

    for pair in ((x, y) for x, y in zip(best, best[1::1])):
        curr = get_area(*pair)
        best_area = max(curr, best_area)

        print(curr, best_area)

    return best_area

import heapq

def max_area(heights):
    lenh = len(heights)

    heap = []

    for i, h in enumerate(heights):
        heapq.heappush(heap, (-h, i))

    maxes = []

    firstn, firsti = heapq.heappop(heap)

    while heap:
        lastn, lasti = heapq.heappop(heap)

        first, last = -firstn, -lastn
        heapq.heappush(
            maxes,
            (-min(first, last), -abs(firsti - lasti))
        )

    return maxes
    return -heapq.heappop(maxes)

def max_area_solution_with_On_space(heights):
    lenh = len(heights)

    left = 0
    right = lenh - 1

    maxes = []

    def area(l, r):
        return (
            min(heights[l], heights[r])
            * abs(l - r)
        )

    while left < right:
        a = area(left, right)
        heapq.heappush(maxes, -a)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return -heapq.heappop(maxes)

def max_area(heights):
    lenh = len(heights)

    left = 0
    right = lenh - 1

    maxes = -1

    def area(l, r):
        return (
            min(heights[l], heights[r])
            * abs(l - r)
        )

    while left < right:
        maxes = max(maxes, area(left, right))

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return maxes




test = [
    max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) # 49
    , max_area([9, 11, 2, 2, 2, 2, 10, 11, 12])
    , max_area([1, 2, 1])
    , max_area([3, 6, 1])
    #, max_area([
    #    *list(range(0, 10000))
    #    , *list(range(10000, 0, -1))
    #])
]


#print(f"({left}, {right}) -> {right - left} * {min(val2, val1)} = {(right - left) * min(val1, val2)}")
"""

    def get_window_pairs(idx):
        window = get_sliding_window(idx)
        return [
            get_height(*gety(i, j))
            for i, j in enumerate(range(window, len(height)))
        ]
1
[1, 8, 6, 2, 5, 4, 8, 3, 7]
 ^  ^
2
[1, 8, 6, 2, 5, 4, 8, 3, 7]
 ^     ^
8
[1, 8, 6, 2, 5, 4, 8, 3, 7]
 ^                       ^



"""

"""
[1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
         ^                    ^
         ----------------------

SOLUTION:
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        maxArea = 0

        while left < right:
            currentArea = min(height[left], height[right]) * (right - left)
            maxArea = max(maxArea, currentArea)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return maxArea

By making these pointer movements, we ensure that we are always exploring containers with the potential for larger areas. The approach is based on the observation that increasing the width of the container can only lead to a larger area if the height of the new boundary is greater.
By following this condition and moving the pointers accordingly, the algorithm explores all possible containers and finds the one with the maximum area.
"""
