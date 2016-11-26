#!/usr/bin/env python
class Solution(object):
    def multiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        data1 = [int(i) for i in num1]
        data2 = [int(i) for i in num2]
        mul = [0 for i in xrange(len(data1)+len(data2)-1)]
        for i in xrange(len(data1)):
            for j in xrange(len(data2)):
                mul[i+j] += data1[i] * data2[j]
        for i in xrange(len(mul)-1,0,-1):
            mul[i-1]  += mul[i]/10
            mul[i]     = mul[i]%10
        for i in xrange(len(mul)):
            if mul[i]:
                return "".join([str(j) for j in mul[i:]])
        return '0'
        #[reduce( lambda x,y: x*10+y, i) for i in array]
        #return reduce( lambda x,y: x*10+y, array2)

if __name__ == '__main__':
    s0 = Solution()
    print s0.multiply("90000000000000000","99000000000000000000000000000000000000")
