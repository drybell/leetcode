"""
A permutation of an array of integers is an arrangement of its members into a sequence or linear order.

For example, for arr = [1,2,3], the following are all the permutations of arr: [1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1].
The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).

For example, the next permutation of arr = [1,2,3] is [1,3,2].
Similarly, the next permutation of arr = [2,3,1] is [3,1,2].
While the next permutation of arr = [3,2,1] is [1,2,3] because [3,2,1] does not have a lexicographical larger rearrangement.
Given an array of integers nums, find the next permutation of nums.

The replacement must be in place and use only constant extra memory.

Example 1:

Input: nums = [1,2,3]
Output: [1,3,2]
Example 2:

Input: nums = [3,2,1]
Output: [1,2,3]
Example 3:

Input: nums = [1,1,5]
Output: [1,5,1]

Strategy:

if is_sorted(nums):
    get_next_permutation

else if is_sorted_desc(nums):
    sort(nums)

else:
    find next max
    move max to front (or swap?)

"""

from functools import reduce

def is_sorted(ns, ascending=True):
    if ascending:
        return reduce(
            lambda prev, new: (
                new
                if prev is not None and new >= prev
                else None
            )
            , ns
            , -100000
        ) is not None
    else:
        return reduce(
            lambda prev, new: (
                new
                if prev is not None and new <= prev
                else None
            )
            , ns
            , 100000
        ) is not None


def next_perm(nums):
    if len(nums) in (0, 1):
        return nums

    if len(nums) == 2:
        return nums.reverse()

    def swap(i, j):
        tmp = nums[j]
        nums[j] = nums[i]
        nums[i] = tmp

    def reverse_j_to_end(j):
        i = len(nums) - 1
        while j < i:
            swap(j, i)
            j += 1
            i -= 1

    def find_next_largest(i):
        j = len(nums) - 1
        while j > i:
            if nums[j] > nums[i]:
                return j

            j -= 1

    def find_currmax(i):
        if i == len(nums) - 2:
            return i

        curr = max(nums[i + 1:])
        for j, num in enumerate(nums[i + 1:]):
            if num == curr: return i + j + 1

        return len(nums) - 1

    def skip_odometer(i):
        if i == 0:
            nums.sort()
        else:
            # if previous is greater than all forward:
            if all(map(lambda x: nums[i - 1] >= x, nums[i + 1:])):
                swap(i - 1, i)
            else:
                next_idx = find_next_largest(i - 1)
                swap(i - 1, next_idx)

            reverse_j_to_end(i)

    def find_next(i):
        if i == len(nums) - 1:
            swap(-1, -2)
        elif is_sorted(nums[i:], False) or i == len(nums) - 2:
            skip_odometer(i)
        elif is_sorted(nums[i:]) and nums[i] not in nums[i + 1:]:
            swap(-1, -2)
        else:
            find_next(find_currmax(i))

    find_next(0)

    return nums

test = [
    next_perm([1,2,3])
    , next_perm([3,2,1])
    , next_perm([2,1,4,3])
    , next_perm([5,4,3,2,1])
    , next_perm([4,5,2,3,1])
    , next_perm([1,3,2])
    , next_perm([2,3,1])
    , next_perm([5,4,7,5,3,2])
    , next_perm([4,2,0,2,3,2,0])
    , next_perm([2,3,1,3,3])
    , next_perm([2,2,7,5,4,3,2,2,1])
    , next_perm([2,1,2,2,2,2,2,1])
]

"""
GRAVEYARD

def find_last_ascending(i):
    j = i + 1
    while j < len(nums):
        prev = nums[j - 1]
        curr = nums[j]
        if curr < prev:
            return j

        j += 1

    return j - 1

def next_perm(nums):
    if len(nums) in (0, 1):
        return nums

    if len(nums) == 2:
        return nums.reverse()

    def swap(i, j):
        tmp = nums[j]
        nums[j] = nums[i]
        nums[i] = tmp

    def modify_subset(i):
        ...

    if is_sorted(nums):
        swap(-1, -2)
    elif is_sorted(nums, False):
        nums.reverse()
    else:
        i = 2
        currhead = nums[0]

        while i < len(nums) - 1:
            prev = nums[i - 1]
            curr = nums[i]



def next_perm(nums):
    if len(nums) in (0, 1):
        return nums

    if len(nums) == 2:
        return nums.reverse()

    def swap(i, j):
        tmp = nums[j]
        nums[j] = nums[i]
        nums[i] = tmp

    def backshift(i):
        for j in range(i, len(nums) - 1):
            swap(j, j + 1)

    def frontshift(i):
        for j in range(len(nums) - 1, i - 1, -1):
            swap(j - 1, j)

    def frontshift_by(i, iters):
        for _ in range(iters):
            frontshift(i)

    def reverse_j_to_end(j):
        i = len(nums) - 1
        while j < i:
            swap(j, i)
            j += 1
            i -= 1

    def find_next_largest(i):
        tmp = nums[i] + 1
        while tmp not in nums[i + 1:]:
            tmp += 1

        for j, num in enumerate(nums[i + 1:]):
            if num == tmp: return i + 1 + j

    def find_last_ascending(i):
        j = i + 1
        while j < len(nums):
            prev = nums[j - 1]
            curr = nums[j]
            if curr < prev:
                return j

            j += 1

        return j - 1

    def find_currmax(i):
        curr = max(nums[i + 1:])
        for j, num in enumerate(nums[i + 1:]):
            if num == curr: return i + j + 1

        return len(nums) - 1

    def skip_odometer(i):
        if i == -1:
            nums.sort()
        else:
            frontshift_by(i, 2)
            reverse_j_to_end(find_currmax(i))

    def find_next(i):
        if i == len(nums) - 1:
            swap(-1, -2)
        elif i == len(nums) - 2:
            backshift(i - 1)
        elif is_sorted(nums[i:], False):
            skip_odometer(i - 1)
        elif is_sorted(nums[i:]):
            swap(-1, -2)
        else:
            find_next(find_currmax(i))

    find_next(0)

    return nums

def backshift(i):
    for j in range(i, len(nums) - 1):
        swap(j, j + 1)

def frontshift(i):
    for j in range(len(nums) - 1, i - 1, -1):
        swap(j - 1, j)

def frontshift_by(i, iters):
    for _ in range(iters):
        frontshift(i)

def backshift_by(i, iters):
    for _ in range(iters):
        backshift(i)


Had a lot of trouble with this one, and spent a lot of time
just trying to come up with good utility functions to identify
the types of operations that would work. I think moving forward
the key elements I was missing was a clear criteria
to build up in order to guide the operations.

I was stuck trying to get backshift/frontshift working when in
reality the solution didn't require them. I also struggled with
the wrong find_next_largest implementation and didn't realize until
too late that starting from the end of the list (since its sorted descending already)
would be much easier than from the beginning.

Solution Points from community:

* We need to find the first decreasing element from the right of the list.
* Then, we need to find the smallest element from the right side that is greater than the first decreasing element.
* We swap these two elements
* Finally we reverse the sublist from the first decreasing element to the end of the list.

Looks like i got the gist of the last 3 points, and failed to identify the first,
which means that I had to add additional is_sorted cases instead of just hunting for
the first decreasing element

"""
