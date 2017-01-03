class Solution(object):
    def largestDivisibleSubset(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        n = len(nums)
        if n<=0:
            return []
        nums.sort()
        pre = [-1] * n
        cnt = [1 ] * n
        ret = []
        maxlen = maxidx = 0
        for i in range(1,n):
            for j in range(i):
                if nums[i]%nums[j]==0:
                    if cnt[j]+1>cnt[i]:
                        pre[i] = j
                        cnt[i] = cnt[j] + 1
            if cnt[i]>maxlen:
                maxlen = cnt[i]
                maxidx = i
        while maxidx>=0:
            ret.append(nums[maxidx])
            maxidx = pre[maxidx]
        return ret
if __name__ == '__main__':
    s0 = Solution()
    print s0.largestDivisibleSubset([1,2,4,8])

