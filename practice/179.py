#!/usr/bin/env python
class Solution:
    # @param {integer[]} nums
    # @return {string}
    def largestNumber(self, nums):
        num_s = [str(s) for s in nums]
        num_s.sort(cmp=lambda x, y: cmp(y+x, x+y))
        ret = ''.join(num_s).lstrip('0')
        if ret=='':
            ret = '0'
        return ret

if __name__ == '__main__':
    s0 = Solution()
    print s0.largestNumber([1,2,3,4,0])
