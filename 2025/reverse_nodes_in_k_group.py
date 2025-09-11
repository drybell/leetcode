"""
Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

Example 1:
Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]

Example 2:
Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]

looks like i'm just swapping at k instead of reversing by k

"""

from utils import ListNode, linked_list

def reverse_k_group(head, k):
    if head is None or head.next is None or k == 1:
        return head

    idx     = 1
    prev    = []
    inner   = []
    swap    = []
    pointer = head

    while pointer is not None:
        # perform the swap
        if idx % k == 0:
            next_pointer = pointer.next

            if inner:
                swap[0].next = next_pointer
                pointer.next = inner[0]
                inner[-1].next = swap[0]
            else:
                swap[0].next = next_pointer
                pointer.next = swap[0]

            if idx == k:
                head = pointer

            if not prev:
                if inner:
                    prev.append(inner[-1].next)
                else:
                    prev.append(pointer.next)
            else:
                prev[0].next = pointer

                if inner:
                    prev[0] = inner[-1].next
                else:
                    prev[0] = pointer.next

            print(f"\n{swap}\n{inner}\n{pointer}\n{head}\n{prev}")
            pointer = next_pointer
            swap = []
            inner = []
        else:
            # add to inner
            if k != 2 and (idx % k == 2 or idx % k == k - 1):
                inner.append(pointer)
            elif idx % k == 1:
                swap.append(pointer)

            pointer = pointer.next

        idx += 1

    return head

"""
        1 -> 2 -> 3 -> 4 -> 5 -> 6
head    |
pointer |
reverse
prev

swap = pointer.next


        1 -> 2 -> 3 -> 4 -> 5 -> 6
head    |
pointer      |
reverse
prev

"""

def reverse_k_group(head, k):
    if head is None or head.next is None or k == 1:
        return head

    idx     = 1
    prev    = None
    reverse = None
    pointer = head

    while pointer is not None:
        if idx % k != 0:
            ...
        elif idx % k == 0:
            prev = pointer
            pointer = pointer.next

        idx += 1

    return head

# NOTE: this version reverses even if a full k group
# is not detected (if len(head) == 7 and k = 4 the last group will
# be reversed)

def get_length(head):
    tmp = head

    i = 1
    while tmp.next is not None:
        tmp = tmp.next
        i += 1

    return i

def reverse_k_group(head, k):
    node = head

    ultimate = None

    idx = 1

    currhead = head
    prevhead = None

    while node.next is not None:
        ultimate = node
        node = node.next

        if idx % k == 0:
            if prevhead is None:
                prevhead = currhead
            else:
                head = ultimate

            currhead = ultimate.next

        else:
            if idx % k == 1 and get_length(ultimate) < k:
                return prevhead or currhead

            ultimate.next = node.next
            node.next = currhead
            currhead = node

            if prevhead is not None:
                head.next = currhead

            node = ultimate

        idx += 1

    return prevhead or currhead


test = [
    reverse_k_group(linked_list([1,2,3,4]), 3)
    , reverse_k_group(linked_list([1,2]), 2)
    , reverse_k_group(linked_list([1,2,3,4,5,6,7,8]), 4)
    , reverse_k_group(linked_list([1,2,3,4,5,6,7,8,9]), 5)
    , reverse_k_group(linked_list([1,2,3]), 4)
    , reverse_k_group(linked_list([1,2,3,4,5]), 2)
    , reverse_k_group(linked_list([1,2,3,4]), 4)
]
