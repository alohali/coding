class Solution(object):
    def minSubArrayLen(self, s, nums):
        """
        :type s: int
        :type nums: List[int]
        :rtype: int
        """
        n = len(nums)
        minlen = n+1
        left = right = sum0 = 0
        while(right<n or (left<right and sum0>=s)):
        	if sum0<s:
        		sum0  += nums[right]
        		right += 1
        	else:
        		if right-left<minlen:
        			minlen = right - left
        		sum0 -= nums[left]
        		left += 1
        if minlen>n:
        	return 0
        else:
 			return minlen

if __name__ == "__main__":
    s0 = Solution()
    print(s0.minSubArrayLen(7,[2,3,1,2,4,3]))