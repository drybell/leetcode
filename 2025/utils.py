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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        base = f"({self.val})"
        if self.left:
            base = f"{self.left} <- {base}"
        if self.right:
            base = f"{base} -> {self.right}"

        return base

def binary_tree(head):
    root = TreeNode(val=head[0])

    curr = root
    cache = []

    for i, val in enumerate(head[1:]):
        tmp = TreeNode(val=val)
        cache.append(tmp)

        if curr.left is None:
            curr.left = tmp

        elif curr.right is None:
            curr.right = tmp

        if (i + 1) % 2 == 0:
            curr = cache.pop(0)

    return root

def linked_list(head):
    root = ListNode(val=head[0])
    curr = root

    for val in head[1:]:
        tmp = ListNode(val=val)
        curr.next = tmp
        curr = tmp

    return root

