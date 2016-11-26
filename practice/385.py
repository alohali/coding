#!/usr/bin/env python
class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        l0 = [i for i in magazine]
        for s in ransomNote:
            if(s in l0):
                l0[l0.index(s)] = 0
            else:
                return False
        return True

if __name__ == '__main__':
    s0 = Solution()
    print s0.canConstruct("aaa","aababb")
