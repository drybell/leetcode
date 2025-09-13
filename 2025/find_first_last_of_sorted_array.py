"""
34. Find First and Last Position of Element in Sorted Array
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/description/

Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
Example 2:

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
Example 3:

Input: nums = [], target = 0
Output: [-1,-1]

Another Binary Search
"""

def search_range(nums, target):
    def get_start_and_end(i):
        idx = i
        while idx > -1 and nums[idx] == target:
            idx -= 1

        if idx != i:
            found = idx + 1
        else:
            found = i

        idx = found
        while idx < len(nums) and nums[idx] == target:
            idx += 1

        if idx != found:
            return [found, idx - 1]
        else:
            return [found, found]

    def traverse(i, j, found=None):
        if (innerlen := j - i) == 0:
            return [-1, -1]

        if innerlen == 1:
            if target == nums[i]:
                return get_start_and_end(i)

            return [-1, -1]

        if innerlen == 2:
            if target == nums[i]:
                return get_start_and_end(i)
            if target == nums[i + 1]:
                return get_start_and_end(i + 1)

            return [-1, -1]

        isodd = innerlen % 2 == 1

        pivot = i + (innerlen // 2)

        #print(nums[i:j], nums[i:pivot], nums[pivot:j], pivot, nums[pivot])

        if target > nums[pivot]:
            return traverse(pivot, j, found)
        elif target == nums[pivot]:
            return get_start_and_end(pivot)
        else:
            return traverse(i, pivot, found)

    return traverse(0, len(nums), [])

test = [
    search_range([5,7,7,8,8,10], 8)
    , search_range([5,7,7,8,8,10], 6)
    , search_range([5,7,7,8,8,9,10], 9)
    , search_range([1,2,5,7,7,8,8,9,10], 7)
    , search_range([1,2,3], 2)
    , search_range([1,1,2,3], 1)
    , search_range([1,1,1,2,3], 1)
]

"""
Notes:

Looks like doing another binary search to practice getting
the pivot index, base/edge cases, and logic down was a good
decision. Doing this again solidified my understanding of
the pitfalls and this one went a lot faster
"""
