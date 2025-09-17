"""
416. Partition Equal Subset Sum
https://leetcode.com/problems/partition-equal-subset-sum/description/

Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.

Example 1:

Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].

Example 2:

Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.

Strategy:

looks like a one pointer

    first, we split the array evenly, and for each iteration
    we check if the subarrays sum to each other

    if we don't find a match, we move the pointer

Second Attempt:
first try didn't work, but I have more information on how to solve.
Only scenario when two subarrays can equal each other is if the
sum of the array is even and the subarrays equal sum(array) / 2

we have to find a combination of elements in the array that sum
up to sum(array) / 2, and the other half would be found automatically


Dynamic Programming is the answer (my most-feared)



"""

def can_partition(nums):
    arrsum = sum(nums)
    arrlen = len(nums)

    if arrlen == 1:
        return False

    if arrsum % 2 == 1:
        return False

    if len(set(nums)) == 1:
        return True

    half = arrsum // 2

    M = [[0] * (half + 1) for i in range(arrlen + 1)]

    # let M(i, j) = max value of partial sum when choosing
    # elements 0 - i

    for subset in range(1, arrlen + 1):
        for partial_sum in range(1, half + 1):
            prev_num = nums[subset - 1]

            if prev_num <= partial_sum:
                # previous number can be included in this partial sum
                # so we add it to the sack by adding it with the
                # solution of the previous subset without that number
                M[subset][partial_sum] = max(
                    prev_num + M[subset - 1][partial_sum - prev_num] # include
                    , M[subset - 1][partial_sum]                     # exclude
                )
            else:
                # previous number can't fit into the partial sum, so we use
                # the previous max sum given the same partial sum constraint
                M[subset][partial_sum] = M[subset - 1][partial_sum]

    return M

test = [
    can_partition([1,5,11,5])
    , can_partition([1,2,3,5])
    #, can_partition([1,1,2,2])
    , can_partition([3,3,6,8,16,16,16,18,20])
    #, can_partition([1,1,1,1])
    #, can_partition([1,2,3,4,5,6,7])
    #, can_partition([1,2,5])
    #, can_partition([14,9,8,4,3,2])
    #, can_partition([1,1,2,5,5,5,5])
    #, can_partition([20,10,9,8,8,3])
    #, can_partition([10,9,9,9,9,8,7,3,1,1])
    #, can_partition([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,97,95])
]

"""
GRAVEYARD

def subsets_sum_to_each_other(arr1, arr2):
    return sum(arr1) == sum(arr2)

def can_partition(nums):
    sorted_nums = sorted(nums)

    def check(i):
        print(sorted_nums[:i], sorted_nums[i:], sum(sorted_nums[:i]), sum(sorted_nums[i:]))
        return subsets_sum_to_each_other(
            sorted_nums[:i], sorted_nums[i:]
        ) or (
            len(sorted_nums[:i]) == len(sorted_nums[i:])
            and len(set(sorted_nums[:i])) == 1
            and len(set(sorted_nums[i:])) == 1
        )

    # naive
    for i in range(1, len(nums)):
        if check(i):
            return True

    return False

def can_partition(nums):
    def currsum(arr):
        if len(arr) == 0:
            return 0

        return sum(arr)

    def get_next(vals, arr, idx, even=False):
        for i, curr in enumerate(vals[idx:]):
            if curr in arr:
                continue

            return i + idx

    arrsum = sum(nums)

    if arrsum % 2 == 1:
        return False

    half = arrsum // 2
    is_half_odd = half % 2 == 1

    sorted_nums = sorted(nums, reverse=True)

    arr  = []
    prev = 0
    i    = 0

    while (curr := currsum(arr)) != half and prev < len(nums):
        newi = get_next(sorted_nums, arr, i, even=True)

        if newi is None:
            arr.pop(0)
            prev += 1
            i = 0
        else:
            arr.append(sorted_nums[newi])
            i = newi + 1

        #print(arr, currsum(arr), half)

    return currsum(arr) == half

def can_partition(nums):
    def get_next(arr, diff):
        for i, val in enumerate(arr):
            if val < diff:
                if (diff - val) not in arr:
                    continue

                return i

        return len(arr) - 1

    arrsum = sum(nums)

    if len(nums) == 1:
        return False

    if arrsum % 2 == 1:
        return False

    if len(set(nums)) == 1:
        return True

    half = arrsum // 2

    deduped = list(set(nums))
    dedupe_sum = sum(deduped)

    diff = dedupe_sum - half

    if diff == 0:
        return True

    for cloned in [
        list(sorted(nums, reverse=True))
        , sorted(deduped, reverse=True)
    ]:

        cache = []

        while len(cloned) > 0:
            diff = sum(cloned) - half
            if diff == 0 or diff in cloned:
                return True
            elif diff < 0:
                if abs(diff) in cache:
                    return True

            print(cloned, diff)
            cache.append(
                cloned.pop(get_next(cloned, diff))
            )

    return False

split choice was interesting to try out
def can_partition(nums):
    arrsum = sum(nums)

    if len(nums) == 1:
        return False

    if arrsum % 2 == 1:
        return False

    if len(set(nums)) == 1:
        return True

    half = arrsum // 2

    arr = []

    topick = sorted(nums, reverse=True)

    found = [False]

    def split_choice(i, arr):
        if sum(arr) == half:
            found[0] = True
            return

        if i == len(nums) - 1:
            return

        if sum(arr) > half:
            return

        if found[0]:
            return

        split_choice(i + 1, [*arr, topick[i]])
        split_choice(i + 1, arr)

    split_choice(0, arr)
    return found[0]



"""
