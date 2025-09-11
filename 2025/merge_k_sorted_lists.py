"""
You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

Example 1:

Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6

Example 2:

Input: lists = []
Output: []

Example 3:

Input: lists = [[]]
Output: []


Naive:

Transpose the linked lists, and check if any are smaller

1,4,5 3,4,5 2,6

1,3,2

cache => [1,2,3]

4,4,2

cache => [1,2,2,3,4,4]

5,5,6

cache => [1,2,2,3,4,4,5,5,6]

Naive is found to be too slow (n^2)

need to use the fact that the lists are sorted

i believe dynamic pointers should be used to minimize
extraneous looping

1,4,5 3,4,5 2,6

pointers = 0,0,0

1,3,2
4,4,6
5,5

just append to cache then sort the cache

    O(n*k) + O(n*klog(n*k)) => O(nlogn)
    ^ sending to cache    ^
                          sorting the cache

    where
        n => list length
        k => worst length of linked list

"""

from utils import ListNode

def linked_list(head):
    root = ListNode(val=head[0])
    curr = root

    for val in head[1:]:
        tmp = ListNode(val=val)
        curr.next = tmp
        curr = tmp

    return root

def merge_k(lists):
    if lists is None or len(lists) == 0 or all(ll is None for ll in lists):
        return None

    cache = []
    counter = 0

    while not all(ll is None for ll in lists):
        for i, ll in enumerate([
            ll for ll in lists
            if ll is not None
        ]):
            curr = ll.val
            lists[i] = ll.next

            if len(cache) == 0:
                cache.append(curr)
            else:
                if curr >= cache[-1]:
                    cache.append(curr)
                else:
                    found = False

                    for idx, cacheval in enumerate(cache[::-1]):
                        if curr >= cacheval:
                            cache.insert(len(cache) - idx, curr)
                            found = True
                            break

                    if not found:
                        cache.insert(0, curr)

        counter += 1

    return linked_list(cache)

def merge_k(lists):
    if lists is None or len(lists) == 0 or all(ll is None for ll in lists):
        return None

    cache = []
    counter = 0

    while not all(ll is None for ll in lists):
        for i, ll in enumerate(lists):
            if ll is None:
                continue

            cache.append(ll.val)
            lists[i] = ll.next

    cache.sort()

    return linked_list(cache)

test = [
    merge_k([
        linked_list([1,4,5])
        , linked_list([3,5,6])
        , linked_list([0,2,7])
    ])
    , merge_k([
        linked_list([4,10,12])
        , linked_list([5,6,8])
        , linked_list([7,9,11])
    ])
]


