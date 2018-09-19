#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.diy_logging.logginghelper import LoggerHelper


@LoggerHelper.log
class log_test:
    def __init__(self):
        self.total = 0

    @LoggerHelper.log_params
    def _add(self, x, y):
        self.total + x + y
        return x + y

    @LoggerHelper.log_params("print加前置str")
    def _print(self, string):
        print("pre:" + string)

    def test_getLogger(self):
        self._logger.DEBUGLogger.info("debug")
        self._logger.BaseLogger.info("info")
        self._logger.BaseLogger.error("error")


if __name__ == '__main__':
    t = log_test()

    t._add(1, 2)
    t._print('test str')

    try:
        print(1 / 0)
    except:
        t._logger.exception()
        print(LoggerHelper.exceptionDetail())
