class Solution(object):
    def calculateMinimumHP(self, dungeon):
        """
        :type dungeon: List[List[int]]
        :rtype: int
        """
        m,n = len(dungeon), len(dungeon[0])

        dp = [[111111111111] * (n+1) for _ in xrange(m+1)]

        dp[m][n-1] = dp[m-1][n] = 1
        for i in xrange(m-1,-1, -1):
            for j in xrange(n-1,-1,-1):
                print i,j
                need = max(min(dp[i+1][j], dp[i][j+1]),1)
                dp[i][j] = need - dungeon[i][j]
        return dp[0][0]

if __name__ == "__main__":
    s0 = Solution()
    print s0.calculateMinimumHP([[1,-3,-1],[-2,-3,-1]])
