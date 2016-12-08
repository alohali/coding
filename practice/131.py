#!/usr/bin/env python

class Solution(object):
    def partition(self, s):
        """
        :type s: str
        :rtype: List[List[str]]
        """
        ret = []
        ele = []
        self.find_part(s,ele,ret)
        return ret

    def isPalindrome(self, string):
        return string == string[::-1]

    def find_part(self, s, ele, ret):
        l = len(s)
        if l==1:
            ret.append(ele[:] + [s])
        elif l==0:
            ret.append(ele[:])
        else:
            for i in xrange(1,l+1):
                if self.isPalindrome(s[:i]):
                    ele.append(s[:i])
                    self.find_part(s[i:], ele, ret)
                    ele.pop()









if __name__ == '__main__':
    s0 = Solution()
    print s0.partition("bb")
    """
[
  ["aa","b"],
  ["a","a","b"]
]
"""
