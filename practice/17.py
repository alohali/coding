#!/usr/bin/env python
class Solution(object):
    table = ['','','abc','def','ghi','jkl','mno','pqrs','tuv','wxyz']
    def letterCombinations(self, digits):
        if digits=="":
            return []
        elif '0' in digits:
            return []
        cnt  = [0 for _ in xrange(len(digits))]
        ele  = [0 for _ in xrange(len(digits))]
        ret = []
        self.insert_data(digits, ele, cnt, ret)
        return ret

    def get_change_pos(self,cnt,digits):
        for i in xrange(len(cnt)-1,-1,-1):
            if cnt[i]<len(self.table[int(digits[i])])-1:
                return i
        return -1

    def change_cnt(self,cnt,digits):
        pos = self.get_change_pos(cnt,digits)
        if pos==-1:
            return -1
        cnt[pos] += 1
        for i in xrange(pos+1,len(cnt)):
            cnt[i] = 0
        return 0

    def insert_data(self, digits, ele, cnt, ret):
        state = 0
        while state!=-1:
            for pos,i in enumerate(digits):
                print pos, i
                ele[pos] = self.table[int(i)][cnt[pos]]
            state = self.change_cnt(cnt,digits)
            print cnt
            ret.append("".join(ele))


if __name__ == '__main__':
    s0 = Solution()
    print s0.letterCombinations("9")

