#!/usr/bin/env python
class Solution(object):
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """

        def pow_helper(x,n):
            if n==1:
                return x
            else:
                temp = pow_helper(x,n/2)
                temp = temp * temp
                if n%2==1:
                    temp *= x
                return temp

        if n==0: 
            return 1
        elif n<0:
            return 1.0/pow_helper(x,-n)
        else:
            return pow_helper(x,n)
            

if __name__ == '__main__':
    s0 = Solution()
    print s0.myPow(3,-3)
