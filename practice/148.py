#!/usr/bin/env python
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):


    def __merge(self,l0,l1):
        if l0.val <= l1.val:
            left = l0
            l0 = l0.next
        else:
            left = l1
            l1 = l1.next
        ret = left
        while l0!=None and l1!=None:
            if l0.val <= l1.val:
                left.next = l0
                l0 = l0.next
            else:
                left.next = l1
                l1 = l1.next
            left = left.next
        if l0==None:
            left.next = l1
        else:
            left.next = l0
        return ret

    def __merge_sort(self, left):
        if left==None or left.next==None:
            return left
        if left.next.next==None:
            if left.val > left.next.val:
                temp = left
                left = left.next
                temp.next = None
            return left

        mid2x = mid = left
        while mid2x!=None and mid2x.next!=None:
            mid = mid.next
            mid2x = mid2x.next.next
        temp = mid.next
        mid.next = None
        l0 = self.__merge_sort(left)
        l1 = self.__merge_sort(temp)

        return self.__merge(l0,l1)
            

    def __quick_sort(self, left,right):
        if left==right or left.next==right:
            return (left,right)

        thrashhold = left.val
        left_temp = left
        right_temp = right
        while left_temp.next!=right:
            if left_temp.next.val <= thrashhold:
                left_temp = left_temp.next
            else:
                temp = left_temp.next
                left_temp.next = left_temp.next.next
                temp.next = right_temp
                right_temp = temp
        temp = left.next
        left.next, right = self.__quick_sort(right_temp,right)

        if left_temp!=left:
            left_temp.next = left
            l, _ = self.__quick_sort(temp, left)
            left = l
        return (left,right)

    def sortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        #l,_ = self.__quick_sort(head, None)
        l = self.__merge_sort(head)
        return l

if __name__ == '__main__':
    l = ListNode(0)
    l1 = ListNode(2)
    l2 = ListNode(1)
    l.next = l1
    l1.next = l2
    s0 = Solution()
    l = s0.sortList(l)
    while l:
        print l.val
        l = l.next
