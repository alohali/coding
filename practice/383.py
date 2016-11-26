#!/usr/bin/env python
class Solution(object):
    def deserialize(self, s):
        """
        :type s: str
        :rtype: NestedInteger
        """
        return self.__parse(s)

    def __parse(self,s):
        if len(s)==0:
            return 99999999999999999999
        if(s[0]>='0' and s[0]<='9' or s[0]=='-'):
            return int(s)
        else:
            return self.__to_list(s[1:-1])
    def __find_list_pos(self,s):
        cnt = 0
        for pos,a  in enumerate(s):
            if a=='[':
                cnt += 1
            elif a==']':
                cnt -= 1
                if not cnt:
                    return pos
        return -1

    def __to_list(self, s):
        ret = []
        pos = 0
        while pos<len(s):
            if s[pos]==',':
                pos+=1
                continue
            elif s[pos]!='[':
                pos2 = s.find(',',pos)
                pos3 = pos2+1
            else:
                pos2 = self.__find_list_pos(s[pos:])+ pos + 1
                pos3 = pos2

            if(pos2<0):
                ret.append(self.__parse(s[pos:]))
                break
            else:
                ret.append(self.__parse(s[pos:pos2]) )
                pos = pos3

        return ret

if __name__ == '__main__':
    s0 = Solution()
    print s0.deserialize("[123,456,[788,799,833],[],[[]],10]")
