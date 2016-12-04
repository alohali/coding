#!/usr/bin/env python

class Solution(object):
    def combinationSum2(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if target<= 0:
            return []
        ret = []
        candidates.sort()
        self.find_num(target, candidates,[],ret,0)
        return ret

    def find_num(self,target, candidates, ele, ret, start_idx):
        if target==0:
            ret.append(ele[:])
        else:
            oldnum = -1
            for idx in xrange(start_idx,len(candidates)):

                num = candidates[idx]
                if num==oldnum:
                    continue
                else:
                    oldnum = num
                if num<=target:
                    ele.append(num)
                    self.find_num(target-num,candidates ,ele,ret, idx+1)
        if ele:
            ele.pop()


if __name__ == '__main__':
    s0 = Solution()
    print s0.combinationSum2([10,1,2,7,6,1,5],8)

