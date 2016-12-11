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
        self.ret = 0
        self.lines, self.adds, self.minus = set(), set(), set()
        self.bt(0, [])
        return self.ret

    def bt(self, num, ele):
        for i in xrange(self.n):
            if i in self.lines or i-num in self.minus or i+num in self.adds:
                continue
            self.lines.add(i)
            self.adds.add(i+num)
            self.minus.add(i-num)
            line = ['.'] * self.n
            line[i] = 'Q'
            ele.append(''.join(line))
            if num == self.n -1:
                self.ret += 1
            else:
                self.bt(num+1, ele)
            ele.pop()
            self.lines.remove(i)
            self.adds.remove(i+num)
            self.minus.remove(i-num)

if __name__ == '__main__':
    s0 = Solution()
    print s0.solveNQueens(4)
