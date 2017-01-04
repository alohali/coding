class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        n = len(prices)
        if n==0:
            return 0
        f = [0] * n
        g = [0] * n
        
        min0 = prices[0]
        for i in range(1,n):
            f[i] = max(f[i-1],prices[i] - min0)
            min0 = min(prices[i],min0)

        max0 = prices[-1]
        for i in range(n-2,0,-1):
            g[i] = max(max0-prices[i+1],g[i+1])
            max0 = max(max0,prices[i+1])

        max0 = 0
        for i in range(n):
            max0 = max(max0, f[i]+g[i])

        return max0


if __name__ == "__main__":
    s0 = Solution()
    print(s0.maxProfit([1,3,2,4]))