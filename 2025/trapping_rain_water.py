"""
42. Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water/description/

Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:

Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:

Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:

n == height.length
1 <= n <= 2 * 104
0 <= height[i] <= 105
"""

MIN_HEIGHT = -1

def trapv1(height):
    left = 0

    hold  = []
    maxes = []

    while height[left] == 0:
        left += 1

    while left < len(height):
        curr = height[left]
        if not maxes or curr > maxes[-1]:
            maxes.append(curr)
            right = left + 1

            while right < len(height):
                curr = height[right]

                if curr < maxes[-1]:
                    hold.append(maxes[-1] - curr)
                else:
                    break

                right += 1

            left = right
        else:
            left += 1

        print(hold, maxes)

    return hold

def trap(height):
    left = 0

    hold  = []
    maxes = []

    while left < len(height) and height[left] == 0:
        left += 1

    if left == len(height):
        return 0

    if all(height[i] > height[i+1] for i in range(len(height) - 1)):
        return 0

    while height and height[-1] == 0:
        height.pop()

    while left < len(height) - 1:
        curr = height[left]
        right = left + 1

        tmpmax = MIN_HEIGHT
        tmpright = right

        while right < len(height):
            nextval = height[right]

            if nextval >= tmpmax:
                tmpmax = nextval
                tmpright = right

            if nextval >= curr:
                break

            right += 1

        if tmpright == left + 1:
            left = tmpright
        else:
            hold.extend([
                min(tmpmax, curr) - h
                for h in height[left + 1:tmpright]
            ])

            left = tmpright

    return sum(hold)

test = [
    trap([0,1,0,2,1,0,1,3,2,1,2,1])
    , trap([4,2,0,3,2,5])
    , trap([4,2,3])
    , trap([5,4,1,2])
    , trap([4,4,4,7,1,0])
    , trap([0,7,1,4,6])
    , trap([4,9,4,5,3,2])
    , trap([0,1,2,0,3,0,1,2,0,0,4,2,1,2,5,0,1,2,0,2])
    , trap([9,6,8,8,5,6,3])
]
