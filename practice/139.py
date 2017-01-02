#!/usr/bin/env python

class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: Set[str]
        :rtype: bool
        """
        f = [False for _ in range(len(s))]
        for i in range(len(s)):
            if s[:i+1] in wordDict:
                f[i] = True
                continue
            for j in range(0,i):
                if f[j] and s[j+1:i+1] in wordDict:
                    f[i] = True
                    break
        return f[-1]

if __name__ == '__main__':
    s0 = Solution()
    print s0.wordBreak("leetcode",["leet", "code"])

