#!/usr/bin/env python

class Solution(object):
    def combinationSum3(self, k, n):
        """
        :type k: int
        :type n: int
        :rtype: List[List[int]]
        """
        ret = []
        self.ele = []
        self.find_num(1,k,n,ret)
        return ret

    def find_num(self,start_idx, k,n, ret):
        if n<k*start_idx or n>9*k:
            return

        if k==1:
            if n<=9 and n>=start_idx:
                ret.append(self.ele[:]+[n])
            else:
                return
        else:
            for idx in xrange(start_idx,9-k+1+1):
                self.ele.append(idx)
                self.find_num(idx+1,k-1,n-idx,ret)
                self.ele.pop()







if __name__ == '__main__':
    s0 = Solution()
    print s0.combinationSum3(3,9)
    """
Input: k = 3, n = 7
[[1,2,4]]
 k = 3, n = 9
 [[1,2,6], [1,3,5], [2,3,4]]"""
