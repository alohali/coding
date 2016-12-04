#!/usr/bin/env python
class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if target<= 0:
            return []

        def find_num(target, candidates, ele, ret, start_idx):
            if target==0:
                ret.append(ele[:])
            #print ele
            for idx in xrange(start_idx, len(candidates)):
                num = candidates[idx]
                if num<=target:
                    ele.append(num)
                    #candidates.pop(idx)
                    find_num(target-num, candidates,ele,ret,idx)
            if ele:
                ele.pop()

        ret = []
        find_num(target,candidates[:], [],ret,0)
        return ret


if __name__ == '__main__':
    s0 = Solution()
    print s0.combinationSum([2, 3, 6, 7],7)

