#!/usr/bin/env python
class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        table = {}
        ret = []
        for s in strs:
            ss = sorted(s)
            ss = ''.join(ss)
            if table.has_key(ss):
                table[ss].append(s)
            else:
                table[ss] = [s]
        for s in table.values():
            ret.append(s)
        return ret




if __name__ == '__main__':
    s0 = Solution()
    print s0.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
