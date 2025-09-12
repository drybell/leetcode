"""
33. Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
Example 2:

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
Example 3:

Input: nums = [1], target = 0
Output: -1

Strategy:

O(log n) means we'll have to do some binary search
or split operations into two pieces

i would assume in this case that we would want
to start our search in the middle of the array,
and continue splitting each search into subarrays
until we identify the value (or return -1).

the trick will be to find where to shim the condition
of flipping the comparison operator when we identify
the rotated section

pivot examples:

odd:
    7,0,1
      ^

    6,7,0
      ^

even:
    6,7,0,1
      ^ ^

    5,6,7,0
      ^ ^
"""

def search(nums, target):
    def find_pivot(i, j):
        if (innerlen := j - i) in (0, 1):
            return None

        isodd = innerlen % 2 == 1

        pivot = i + (innerlen // 2)

        if not isodd and i != 0:
            pivot += 1

        if pivot >= len(nums):
            return None

        print(nums[i:j], pivot)

        if nums[pivot - 1] > nums[pivot]:
            return pivot
        elif pivot + 1 < len(nums) and nums[pivot] > nums[pivot + 1]:
            return pivot + 1 if isodd else pivot
        elif nums[i] > nums[pivot]:
            return find_pivot(i, pivot)
        else:
            return find_pivot(pivot, j)

    def traverse(i, j):
        if (innerlen := j - i) == 0:
            return -1

        if innerlen == 2:
            if target == nums[i]:
                return i
            elif target == nums[i + 1]:
                return i + 1
            return -1

        isodd = innerlen % 2 == 1

        pivot = i + (innerlen // 2)

        if not isodd and i != 0:
            pivot += 1

        if target > nums[pivot]:
            return traverse(pivot + 1 if isodd else pivot, j)
        elif target == nums[pivot]:
            return pivot
        elif not isodd and target == nums[pivot - 1]:
            return pivot - 1
        else:
            return traverse(i, pivot)

    if len(nums) == 1:
        return 0 if target in nums else -1
    if nums[0] == target:
        return 0
    if nums[-1] == target:
        return len(nums) - 1

    pivot = find_pivot(0, len(nums))

    print(nums, pivot)

    if pivot is not None:
        if target == nums[pivot]:
            return pivot
        if target > nums[-1]:
            return traverse(0, pivot)
        else:
            return traverse(pivot, len(nums))
    else:
        return traverse(0, len(nums))

test = [
    search([4,5,6,7,0,1,2], 0)
    , search([4,5,6,7,0,1,2], 3)
    , search([4,5,6,7,8,9,10,11,12,0,1,2,3], 3)
    , search([4,5,6,7,8,9,10,11,12,13,0,1,2], 3)
    , search([0], 3)
    , search([0, 1], 1)
    , search([0, 1, 2], 5)
    , search([3, 1], 3)
    , search([5, 3, 1], 3)
    , search([5, 1, 3], 1)
    , search([5, 1, 3], 0)
    , search([5, 1, 3], 3)
    , search([15,16,19,20,25,1,3,4,5,7,10,14], 25)
]

"""
Notes:

This one took a quick time setting up the overarching conditionals
and getting binary search working.

I wasted too much time trying to identify the missing cases,
along with the small length scenarios (lists of lengths 1 - 3)

There's definitely a way to do this by just continuing recursing
after finding the pivot or within find_pivot.
"""
