"""
Given an integer array nums sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same.

Since it is impossible to change the length of the array in some languages, you must instead have the result be placed in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.

Return k after placing the final result in the first k slots of nums.

Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
If all assertions pass, then your solution will be accepted.


TESTS:


1, 1, 2, 2, 2, 3, 5, 6, 6, 6, 7, 7, 7
^
|
cur = 1


1, 1, 2, 2, 2, 3, 5, 6, 6, 6, 7, 7, 7
   ^
   |
   cur = 1, count = 2


1, 1, 2, 2, 2, 3, 5, 6, 6, 6, 7, 7, 7
      ^
      |
      cur = 2, count = 1


1, 1, 2, 2, 2, 3, 5, 6, 6, 6, 7, 7, 7
         ^
         |
         cur = 2, count = 2


1, 1, 2, 2, 2, 3, 5, 6, 6, 6, 7, 7, 7
            ^
            |
            cur = 2, count = 3
            remove entry, k += 1


1, 1, 2, 2, 3, 5, 6, 6, 7, 7


"""

from typing import List

def remove_dupes(nums : List[int]) -> int:
    k     = 0
    count = 1
    prev  = -9999999
    i     = 0

    while i < len(nums):
        print(nums[i], count, prev, k, i)
        if (cur := nums[i]) != prev:
            count = 1
            prev  = cur
            i += 1
        elif cur == prev:
            print(cur, count, prev, i, k)
            count += 1
            if count > 2:
                nums.pop(i)
                k += 1
            else:
                i += 1

    return k


test = [1,1,2,2,2,3,5,6,6,6,7,7,7]
k = remove_dupes(test)
print(k, test)
assert k == 3
assert test == [1,1,2,2,3,5,6,6,7,7]

test = [1,1,1,2,2,3]
k = remove_dupes(test)
print(k, test)
assert k == 1
assert test == [1,1,2,2,3]

test = [0,0,1,1,1,1,2,3,3]
k = remove_dupes(test)
print(k, test)
assert k == 2
assert test == [0,0,1,1,2,3,3]
