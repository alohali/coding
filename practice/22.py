#!/usr/bin/env python
class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        ret = []
        ele = [0 for _ in xrange(n*2)]
        self.f(0,0,n,ret,ele)
        return ret

    def f(self,left,right,len,l, ele):
        if(right==len):
            l.append("".join(ele))
            ele[len*2-1] = 0
            return 
        if(left<len):
            ele[left+right] = "("
            self.f(left+1,right,len, l, ele)
        if(right<left):
            ele[left+right] = ")"
            self.f(left,right+1,len, l, ele)




if __name__ == '__main__':
    s0 = Solution()
    print s0.generateParenthesis(3)
