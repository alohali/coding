class Solution(object):
    def __copy(self, l_src, l_dst, idx):

        for ele in l_src:
            ele_new = ele[:]
            ele_new.append(idx)
            l_dst.append(ele_new)

    def __dfs(self, idxs, s):
        ret = []
        for idx in idxs:
            s0 = s[0:idx[0]+1]
            start = idx[0]+1
            for i in xrange(1,len(idx)):
                ii = idx[i] 
                s0 += " " + s[start: ii+1]
                start = ii+1
            ret.append(s0)
        return ret

    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: List[str]
        """
        n = len(s)
        flag = [False] * n
        dp = [[] for _ in xrange(n)]

        for i in xrange(n):
            if s[:i+1] in wordDict:
                flag[i]=True
            for j in xrange(i):
                if flag[j] and (s[j+1:i+1] in wordDict):
                    flag[i] = True
        if not flag[-1]:
            return []
            
        for i in xrange(n):
            if s[:i+1] in wordDict:
                dp[i].append([i])
            for j in xrange(i):
                if flag[j] and (s[j+1:i+1] in wordDict):
                    self.__copy(dp[j],dp[i],i)

        return self.__dfs(dp[-1], s)



s0 = Solution()
print s0.wordBreak("catsanddog",["cat", "cats", "and", "sand", "dog"])
