class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        sta = []
        idx = total = 0

        while(idx<len(height)):
            val = height[idx]
            if len(sta)==0 or val<height[sta[-1]]:
                sta.append(idx)
                idx += 1
            else:
                bot = sta.pop()
                if len(sta)>0:
                    total += (min(height[sta[-1]],val) - height[bot]) * (idx - sta[-1] - 1)
        return total


if __name__ == '__main__':
    s0 = Solution()
    print s0.trap([0,1,0,2,1,0,1,3,2,1,2,1])
