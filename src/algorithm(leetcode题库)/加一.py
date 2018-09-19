#!/user/bin python
# -*- coding:utf-8 -*-  
import sys
import os


class Solution:
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        # index = -1
        # digits[index] += 1
        # while True:
        #     try:
        #         num = digits[index]
        #     except:
        #         break
        #     else:
        #         if num == 10:
        #             digits[index] = 0
        #             try:
        #                 digits[index - 1] += 1
        #             except:
        #                 digits.insert(0, 1)
        #                 break
        #
        #         index -= 1
        # return digits

        datastr = "".join([str(i) for i in digits])
        data = int(datastr) + 1
        return [int(i) for i in str(data)]


if __name__ == '__main__':
    print(Solution().plusOne([8, 9, 9, 9]))
