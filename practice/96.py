# Definition for a binary tree node.
class TreeNode(object):
     def __init__(self, x):
         self.val = x
         self.left = None
         self.right = None

class Solution(object):
    def generateTrees(self, n):
        """
        :type n: int
        :rtype: List[TreeNode]
        """
        if n<=0:
            return []
        ret = [[None], [TreeNode(1)]]

        for i in range(2,n+1): #ith dp
            dp = []
            for j in range(1,i+1):# choose root
                for left in ret[j-1]:
                    for right in ret[i-j]:
                        root = TreeNode(j)
                        root.left  = self.copy_node(left )
                        root.right = self.copy_node(right)
                        dp.append(root)
            ret.append(dp)

        return ret[n]

    def copy_node(self, node, offset):
        if node==None:
            return None
        new_node = TreeNode(node.val + offset)
        new_node.left  = self.copy_node(node.left, offset)
        new_node.right = self.copy_node(node.right, offset)
        return new_node


if __name__ == '__main__':
    s0 = Solution()
    print s0.generateTrees(1)
