#!/usr/bin/env python

class Solution(object):
    def restoreIpAddresses(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        ret = []
        ele = ['' for _ in xrange(4)]
        self.f(0,s,ele,ret)
        return ret

    def f(self,n,s,ele,ret):
        if len(s)>(4-n)*3 or len(s)<(4-n):
            return
        elif n==3:
            if s[0]=='0' and len(s)!= 1:
                return
            elif int(s)<256:
                ele[n] = s
                ret.append(".".join(ele))
                return
        for i in xrange(3):
            temp = s[0:i+1]
            if(int(temp)>=256):
                continue
            elif temp[0]=='0' and len(temp)!=1:
                continue
            else:
                ele[n] = temp
                self.f(n+1,s[i+1:],ele,ret)


if __name__ == '__main__':
    s0 = Solution()
    print s0.restoreIpAddresses("010010")
