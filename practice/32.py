class Solution(object):
    def longestValidParentheses(self, s):
        if s=="":
            return 0
        q0 = []
        maxlen = 0
        last_len  = [0] * len(s)
        if s[0] == '(':
            q0.append((0,0))
        for i in xrange(1,len(s)):
            if s[i]=='(':
                q0.append((i,last_len[i-1]))
            elif len(q0)>0:
                pos0,last = q0.pop()
                last_len[i] = i - pos0 + 1 + last
                maxlen = max(maxlen, last_len[i])

        return maxlen
