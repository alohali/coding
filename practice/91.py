
class Solution(object):
    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """
        if len(s) == 0 or s[0] =='0':
            return 0
        elif len(s) == 1:
            return 1

        n, num = len(s), [1] * len(s)
        if s[1]=='0':
            if s[0] not in '12':
                return 0
        elif int(s[0:2])<27:
            num[1] = 2

        for i in xrange(2,n):
            if s[i]=='0':
                if s[i-1]=='0' or int(s[i-1])>2:
                    return 0
                else:
                    num[i] = num[i-2]
            elif int(s[i-1:i+1])<27 and s[i-1]!='0':
                num[i] = num[i-2] + num[i-1]
            else:
                num[i] = num[i-1]
        return num[-1]

if __name__ == '__main__':
    s0 = Solution()
    print s0.numDecodings("101")
