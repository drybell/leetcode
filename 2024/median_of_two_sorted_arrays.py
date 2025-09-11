"""
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
"""
from typing import List


"""

[1,2,    4,5,            10,12,     20,     25]
[     3,      6,  8,  9,        15,     22]

[1,2,[3],4,5,[6],[8],[9],10,12,[15],20,[22],25]

get_next -> [1, ...], [2, ...]

pop from each list given the next value


"""


def prob(nums1 : List[int], nums2 : List[int]) -> float:
    total_len = len(nums1 + nums2)
    is_even   = total_len % 2 == 0
    halfway   = total_len // 2 + 1

    MAX = 10000000

    res = []

    while (nums1 or nums2) and len(res) < halfway:
        if not nums1:
            nums1 = [MAX]
        if not nums2:
            nums2 = [MAX]

        res.append(nums1.pop(0) if nums1[0] < nums2[0] else nums2.pop(0))

    return res[-1] if not is_even else (res[-2] + res[-1]) / 2
