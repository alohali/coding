#!/usr/bin/env python
class Solution(object):
    
    def valid(self, root, leftmax, rightmin):
        if not root:
            return True
        if not root.left and not root.right:
            return True
        if root.left:
            
            if root.left.val >= root.val:
                return False
            if rightmin and root.left.val >= rightmin.val:
                return False
            if leftmax and root.left.val <= leftmax.val:
                return False
        if root.right:
            if root.right.val <= root.val:
                return False
            if leftmax and root.right.val <= leftmax.val:
                return False
            if rightmin and root.right.val >= rightmin.val:
                return False
        return self.valid(root.left, leftmax, root) and self.valid(root.right, root, rightmin)
        
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        return self.valid(root, None, None)
        
