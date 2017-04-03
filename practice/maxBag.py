#!/usr/bin/env python

class Solution(object):
    def maxBag(self, v_list, maxweight):
        """
            v_list: (n,2): [0]:value, [1]:weight
            maxvalue: int
            rtype: int
        """
        n,m = len(v_list)+1,maxweight+1

        dp = [[0] * m for _ in xrange(n)]
        for i in xrange(1,n):
            for w in xrange(1,m):
                if v_list[i-1][1]>w:
                    dp[i][w] = dp[i-1][w]
                else:
                    dp[i][w] = max(dp[i-1][w],dp[i-1][w-v_list[i-1][1]] + v_list[i-1][0])

        print dp
        return dp[n-1][m-1]





if __name__ == '__main__':
    s0 = Solution()
    print s0.maxBag([[60,1],[100,2],[120,3]],5)
