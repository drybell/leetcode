"""
226. Invert Binary Tree
https://leetcode.com/problems/invert-binary-tree/description/

Given the root of a binary tree, invert the tree, and return its root.

Example 1:
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Example 2:
Input: root = [2,1,3]
Output: [2,3,1]
Example 3:

Example 3:
Input: root = []
Output: []
"""
from utils import binary_tree, TreeNode

def invert_tree(root):
    def traverse(head):
        if head.left is None and head.right is None:
            return

        tmp = head.left
        head.left = head.right
        head.right = tmp

        if head.left:
            traverse(head.left)
        if head.right:
            traverse(head.right)

    copy = root
    traverse(copy)
    return root

test = [
    invert_tree(binary_tree([4,2,7,1,3,6,9]))
]
