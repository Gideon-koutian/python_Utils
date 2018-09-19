#!/user/bin python
# -*- coding:utf-8 -*-
import sys
import os


class Solution:
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        data = []

        if numRows == 0:
            return data

        for i in range(1, numRows + 1):
            temp = []

            if i / 2 > 1:
                temp.append(1)
                for j in range(1, i - 1):
                    temp.append(data[i - 2][j - 1] + data[i - 2][j])
                temp.append(1)
            else:
                for j in range(0, i):
                    temp.append(1)

            data.append(temp)
        return data


if __name__ == '__main__':
    for i, val in enumerate(Solution().generate(3)):
        print(i, val)
        pass
