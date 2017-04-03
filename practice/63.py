#!/usr/bin/env python
class Solution(object):
    def uniquePathsWithObstacles(self, obstacleGrid):
        """
        :type obstacleGrid: List[List[int]]
        :rtype: int
        """
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        path = [[0] * n for i in xrange(m)] 
        for i in xrange(n):
            if obstacleGrid[0][i]:
                path[0][i] = 0
                break
            else:
                path[0][i] = 1
        for i in xrange(m):
            if obstacleGrid[i][0]:
                path[i][0] = 0
                break
            else:
                path[i][0] = 1

        for i in xrange(1,m):
            for j in xrange(1,n):
                if obstacleGrid[i][j]:
                    path[i][j] = 0
                else:
                    path[i][j] = path[i-1][j] + path[i][j-1]

        return path[-1][-1]

if __name__ == '__main__':
    s0 = Solution()
    print s0.uniquePathsWithObstacles([  [0,0,0],  [0,1,0],  [0,0,0]])



        
