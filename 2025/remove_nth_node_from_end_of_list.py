"""
Given the head of a linked list, remove the nth node from the end of the list and return its head.

Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
Example 2:

Input: head = [1], n = 1
Output: []
Example 3:

Input: head = [1,2], n = 1
Output: [1]

"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def to_list(self, tmp=None):
        if tmp is None:
            tmp = []

        if self.next is None:
            return [*tmp, self.val]

        tmp.append(self.val)
        return self.next.to_list(tmp)

    def __repr__(self):
        return f"Node({self.val})"

def linked_list(head):
    root = ListNode(val=head[0])
    curr = root

    for val in head[1:]:
        tmp = ListNode(val=val)
        curr.next = tmp
        curr = tmp

    return root

def remove_nth_from_end(head, n):
    visited = []
    curr = head

    for i in range(10000):
        visited.append(curr)

        if curr.next is None:
            break

        curr = curr.next

    next_idx = (-1 * n) + 1
    prev_idx = (-1 * n) - 1

    if len(visited) == 1:
        return None

    if next_idx == 0:
        visited[prev_idx].next = None
    elif n == len(visited):
        head = visited[1]
        return head
    else:
        visited[prev_idx].next = visited[next_idx]

    return head



test = [
    remove_nth_from_end(linked_list([1,2,3,4,5]), 2)
    , remove_nth_from_end(linked_list([1]), 1)
]
