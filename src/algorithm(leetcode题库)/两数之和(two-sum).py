#!/user/bin python
# -*- coding:utf-8 -*-
import sys
import os


# https://leetcode-cn.com/problems/two-sum/description/
class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # for i in range(0, len(nums)):
        #     temp = target - nums[i]
        #
        #     if temp in nums:
        #         if nums.index(temp) is not i:
        #             return [i, nums.index(temp)]
        #         # 如果对多个相同值得返回顺序有要求，否则上面的if足够满足
        #         else:
        #             if nums.count(temp) > 1:
        #                 del nums[i]
        #                 return [i, nums.index(temp) + 1]

        # temp = dict()
        # for i in range(len(nums)):
        #     if nums[i] in temp:
        #         return [temp.get(nums[i]), i]
        #     temp[target - nums[i]] = i

        temp = {}
        for index, val in enumerate(nums):
            if target - val in temp:
                return temp[target - val], index
            temp[val] = index


if __name__ == '__main__':
    print(Solution().twoSum([3, 3], 6))
#     finish
