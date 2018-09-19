#!/user/bin python
# -*- coding:utf-8 -*-  
import sys
import os


class Solution:

    @classmethod
    def removeDuplicates(cls, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        data = set()
        i = 0

        while i < len(nums):
            try:
                if nums[i] not in data:
                    data.add(nums[i])
                else:
                    del nums[i]
                    continue
            except IndexError:
                break
            else:
                i += 1

        return len(nums)

    def removeDuplicates1(self, nums: list):
        """
        :type nums: List[int]
        :rtype: int
        """
        i = 0
        while True:
            try:
                a = nums[i]
                b = nums[i + 1]
            except:
                break
            else:
                if a == b:
                    del nums[i + 1]
                else:
                    i += 1
        return len(nums)


if __name__ == '__main__':
    s = Solution()
    print(s.removeDuplicates1([0, 0, 1, 1, 1, 2, 2, 3, 3, 4]))
