#!/usr/bin/env python
class Solution(object):

    def  find_pos(self, a1,a2,l,r):
        i = (l + r)//2
        j = (self.n + self.m -1 )//2 - i - 1

        if i<self.n-1 and a1[i+1]<a2[j]:
            return self.find_pos(a1,a2,i+1,r)
        elif i>=0 and a1[i]>a2[j+1]:
            return self.find_pos(a1,a2,min(l,i-1),i-1)
        else:
            if j<0:
                maxLeft = a1[i]
            elif i<0:
                maxLeft = a2[j]
            else:
                maxLeft = max(a1[i],a2[j])
            if (self.n+self.m) % 2==1:
                print i,j
                return maxLeft
            print i,j

            if i==self.n-1:
                minRight = a2[j+1]
            elif j==self.m-1:
                minRight = a1[i+1]
            else:
                minRight = min(a1[i+1],a2[j+1])
            return (minRight + maxLeft)/2.0

    def mid(self, num):
        if self.m == 0:
            return 0
        elif self.m % 2==1:
            return num[self.m // 2]
        else:
            return (num[self.m // 2] + num[self.m // 2 - 1])/2.0

    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """

        self.n = min(len(nums1),len(nums2))
        self.m = max(len(nums1),len(nums2))

        if len(nums1)<=len(nums2):
            if self.n == 0:
                return self.mid(nums2)
            else: 
                return self.find_pos(nums1,nums2,0,len(nums1)-1)
        else:
            if self.n == 0:
                return self.mid(nums1)
            else:
                return self.find_pos(nums2,nums1,0,len(nums2)-1)

if __name__ == '__main__':
    s0 = Solution()
    print s0.findMedianSortedArrays([1,2],[3,4])



        
