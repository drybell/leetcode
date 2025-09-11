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
        return f"{self.val} -> {self.next}"


def linked_list(head):
    root = ListNode(val=head[0])
    curr = root

    for val in head[1:]:
        tmp = ListNode(val=val)
        curr.next = tmp
        curr = tmp

    return root

