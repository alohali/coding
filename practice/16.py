class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        n = len(nums)
        if n<3:
        	return []
        else:
        	nums.sort()
        	ret = nums[0]+ nums[1]+nums[2]
        	minDis = target - ret

        def finddis(pos, val):
        	l,r = pos+1,n-1
        	minp = val - nums[l] - nums[r]
    		real = nums[l] + nums[r]
        	while(l<r):
        		dis = val - nums[l] - nums[r]
        		if abs(dis)<abs(minp):
        			minp = dis   
        			real = nums[l] + nums[r]  			
    			if dis==0:
    				break
        		elif dis<0:
        			r-=1
        		else:
        			l+=1
        	return minp,real

        for i in xrange(n-2):
        	mind,rv = finddis(i,target - nums[i])
        	if abs(mind)<abs(minDis):
        		minDis = mind
        		ret = rv+nums[i]
        	if minDis==0:
        		break
        return ret

s0 = Solution()
print s0.threeSumClosest([1,1,1,0],-100)