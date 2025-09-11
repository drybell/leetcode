"""
Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)

Example 1:
Input: head = [1,2,3,4]

Output: [2,1,4,3]

Example 2:

Input: head = []

Output: []

Example 3:

Input: head = [1]

Output: [1]

Example 4:

Input: head = [1,2,3]

Output: [2,1,3]



head = 1 -> 2 -> 3 -> 4 -> None

pairs[0] = 1 -> 2 -> 3 -> 4 -> None
pointer  = 2 -> 3 -> 4 -> None

swap

pairs[0] = 1 -> 3 -> 4 -> None
pointer  = 2 -> 1 -> 3 -> 4 -> None

head = pointer
head = 2 -> 1 -> 3 -> 4 -> None

2 -> 1 -> 3 -> 4 -> None
          ^
          pointer

pairs[0] = 3 -> 4 -> None
pointer  = 4 -> None

swap

pairs[0] = 3 -> None
pointer  = 4 -> 3 -> None

2 -> 1 -> pairs[0]
     ^

the dangerous trap was missing the previous pointer
that preceded the swapped pair. since that pointer
was previously referencing pair[0], when modifying
pair[0] that would trim the overall list by dropping
pair[0]

Holding the previous node prior to the swapped pair
alleviated this issue
"""

from utils import ListNode, linked_list

def swap_pairs(head):
    if head is None or head.next is None:
        return head

    idx     = 1
    prev    = []
    pairs   = []
    pointer = head

    while pointer is not None:
        if idx % 2 == 0:
            next_pointer = pointer.next

            pairs[0].next = next_pointer
            pointer.next  = pairs[0]

            if idx == 2:
                head = pointer

            if not prev:
                prev.append(pointer.next)
            else:
                prev[0].next = pointer
                prev[0] = pointer.next

            pointer = next_pointer
            pairs = []
        else:
            pairs.append(pointer)
            pointer = pointer.next

        idx += 1

    return head


test = [
    swap_pairs(linked_list([1,2,3,4]))
    , swap_pairs(linked_list([1,2,3,4,5,6,7,8]))
    , swap_pairs(linked_list([1,2,3,4,5,6,7,8,9]))
    , swap_pairs(linked_list([1,2,3]))
]
