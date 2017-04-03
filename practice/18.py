class Solution(object):
        
    def __twoSum(self,nums,target,left,ele,arr):
        l,r = left,self.n - 1
        while l<r:
            if nums[l]>target/2.0 or nums[r]<target/2.0:
                break

            if l!=left and nums[l]==nums[l-1]:
                l += 1
                continue
            if r!=self.n - 1 and nums[r]==nums[r+1]:
                r -= 1
                continue
            if nums[l]+nums[r]==target:
                ele[2],ele[3] = nums[l],nums[r]
                arr.append(ele[:])
                l+=1
                r-=1
            elif nums[l]+nums[r]<target:
                l+=1
            else:
                r-=1




    def fourSum(self, nums, target):
        self.n = len(nums)
        nums.sort()
        arr = []
        ele = [0,0,0,0]
        for i in xrange(self.n-3):            
            if nums[i]>target/4.0:
                break
            if i>0 and nums[i]==nums[i-1]:
                continue
            for j in xrange(i+1,self.n-2):       
                if nums[j]>(target-nums[i])/3.0:
                    break
                if j>i+1 and nums[j]==nums[j-1]:
                    continue
                ele[0],ele[1] = nums[i],nums[j]
                self.__twoSum(nums,target-nums[i]-nums[j],j+1,ele,arr)
        return arr



s0 = Solution()
print s0.fourSum([3,1,4,2,5,-4,2,4,-5],-12)
