#!/usr/bin/env python
# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def deleteNode(self, root, key):
        """
        :type root: TreeNode
        :type key: int
        :rtype: TreeNode
        """
        node = root
        parent = None
        while node and node.val!=key:
            parent = node
            if node.val < key:
                node = node.right
            else:
                node = node.left
        if None==node:
            return root
        if node.left==None:
            if parent == None:
                root = node.right
            else:
                if parent.right.val == node.val:
                    parent.right = node.right
                else:
                    parent.left = node.right
        else:
            if parent == None:
                root = node.left
            else:
                if parent.right.val == node.val:
                    parent.right = node.left
                else:
                    parent.left = node.left

            if node.right!=None:
                temp = node.left
                while temp.right:
                    temp = temp.right
                temp.right = node.right
        return root
