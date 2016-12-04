#!/usr/bin/env python

class Solution(object):

    def findLadders(self, beginWord, endWord, wordlist):
        """
        :type beginWord: str
        :type endWord: str
        :type wordlist: Set[str]
        :rtype: List[List[int]]
        """
        self.endWord = endWord
        self.beginWord = beginWord
        self.wordlist = wordlist
        q = [beginWord,""]
        next_layer = []
        self.parent = {beginWord:[], endWord:[]}
        for i in wordlist:
            self.parent[i] = []
        find_end = False
        while q:
            e = q.pop(0)
            if e=="":
                if find_end:
                    break
                if q:
                    q.append("")
                for i in next_layer:
                    wordlist.remove(i)
                next_layer = []
                continue

            for i in range(len(e)):
                left = e[:i]
                right = e[i + 1:]
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if e[i] != c:
                        nextWord = left + c + right
                        if nextWord==endWord:
                            self.parent[nextWord].append(e)
                            find_end = True
                        elif nextWord in wordlist:
                            self.parent[nextWord].append(e)
                            if not nextWord in next_layer:
                                q.append(nextWord)
                                next_layer.append(nextWord)
        if not find_end:
            return []
        ret = []
        self.find_path(endWord,[],ret)
        return ret
                            
    def find_path(self, endWord, ele, ret):
        ele.append(endWord)
        if endWord==self.beginWord:
            ret.append(ele[::-1])
        else:
            for parent in self.parent[endWord]:
                self.find_path(parent,ele, ret)
        ele.pop()

if __name__ == '__main__':
    s0 = Solution()
    beginWord = "hot"
    endWord = "dog"
    wordList = ["hot","dog"]
    print s0.findLadders(beginWord,endWord,wordList)

