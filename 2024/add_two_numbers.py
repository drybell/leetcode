"""
You are given two non-empty linked lists representing two
non-negative integers. The digits are stored in reverse order,
and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero,
except the number 0 itself.

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]
Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
"""

from typing import List
import numpy as np

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def toint(self):
        tmp = self
        res = []
        while tmp:
            res.append(str(tmp.val))
            tmp = tmp.next

        return int(''.join(reversed(res)))

    @classmethod
    def fromint(cls, i : int):
        l = list(reversed([int(j) for j in list(str(i))]))
        base = cls()
        tmp  = base
        for i, val in enumerate(l):
            base.val  = val
            if i == len(l) - 1:
                break

            base.next = cls()
            base = base.next

        return tmp


def prob(l1 : List[int], l2 : List[int]) -> List[int]:
    tmp = []
    carry_over = 0
    for val1, val2 in zip(l1, l2):
        res = val1 + val2 + carry_over
        if res >= 10:
            res = res % 10
            carry_over = 1
        else:
            carry_over = 0

        tmp.append(res)

    lenl1 = len(l1)
    lenl2 = len(l2)

    if lenl1 == lenl2:
        tmp.append(1) if carry_over == 1 else _
    else:
        extra = l1 if lenl1 > lenl2 else l2
        tmp.append(extra[min(lenl1, lenl2)] + carry_over)
        tmp.extend(extra[min(lenl1, lenl2) + 1:])

    return tmp

def prob2(l1 : ListNode, l2 : ListNode) -> ListNode:
    tmp = ListNode()
    root = tmp
    carry_over = 0
    while l1 is not None or l2 is not None:
        val1 = l1.val if l1 is not None else 0
        val2 = l2.val if l2 is not None else 0

        res  = val1 + val2 + carry_over
        if res >= 10:
            res = res % 10
            carry_over = 1
        else:
            carry_over = 0

        tmp.val  = res
        tmp.next = ListNode()
        tmp      = tmp.next

        l1 = l1.next if l1 is not None else None
        l2 = l2.next if l2 is not None else None

    if carry_over == 1:
        tmp.val = 1

    return root


def test():
    ints = np.random.randint(1, 10000, (100, 2))

    for i1, i2 in ints:
        l1 = ListNode.fromint(i1)
        l2 = ListNode.fromint(i2)
        res = prob2(l1, l2).toint()
        expected = i1 + i2
        print(f"{i1} + {i2} =    {expected}")
        print(f"                 {res}")
        print()
        assert res == expected


