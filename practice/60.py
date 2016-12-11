#!/usr/bin/env python
class Solution(object):
    def solveNQueens(self, n):
        """
        :type n: int
        :rtype: List[List[str]]
        """
        if n<= 0:
            return []
        self.n = n
        ret = []
        self.lines = set()
        self.bt(0, [],ret)
        return ret

    def checkline(self, ele, h, w):
        for i in xrange(1,h+1):
            if w-i>=0 and ele[h-i][w-i]=='Q':
                return False
            elif w+i<self.n and ele[h-i][w+i]=='Q':
                return False
        return True

    def insert(self, ele, ret):
        temp = [ele[i][:] for i in xrange(self.n)]
        ret.append(temp)

    def bt(self, num, ele, ret):
        for i in xrange(self.n):
            if i in self.lines:
                continue
            if not self.checkline(ele, num, i):
                continue

            self.lines.add(i)
            line = ['.'] * self.n
            line[i] = 'Q'
            ele.append(''.join(line))
            if num == self.n -1:
                self.insert(ele, ret)
            else:
                self.bt(num+1, ele, ret)
            ele.pop()
            self.lines.remove(i)

if __name__ == '__main__':
    s0 = Solution()
    r= s0.solveNQueens(4)
    for i in xrange(len(r)):
        print r[i]
