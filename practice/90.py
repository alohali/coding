#!/usr/bin/env python
class Solution(object):
    def subsetsWithDup(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        arr = [[]]
        ele = []
        nums.sort()
        self.bt(nums,ele,arr)
        return arr

    def bt(self, nums, ele, arr):
        if len(nums)==0:
            return
        for idx,num in enumerate(nums):
            if idx>0 and num==nums[idx-1]:
                continue
            ele.append(num)
            arr.append(ele[:])
            self.bt(nums[idx+1:],ele,arr)
            ele.pop()



if __name__ == '__main__':
    s0 = Solution()
    print s0.subsetsWithDup([1,2,2,3])
