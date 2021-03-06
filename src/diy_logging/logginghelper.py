#!/usr/bin/env python
import os
import sys
import linecache
import logging
from logging import config
import yaml
import pkgutil
from functools import wraps
import textwrap
from src.diy_logging.setting import LOGGING_CONFIG, LOGGING_JERTY, LOGGING_ERROR

Factory = None
textWrapper = textwrap.TextWrapper(width=120, break_long_words=True, replace_whitespace=False,
                                   subsequent_indent="      ")


class LoggerHelper:

    @staticmethod
    def getLoggerFactory():
        """
        单例模式，返回LoggerFactory
        :return:
        """
        global Factory

        if Factory is None:
            Factory = LoggerHelper()

        if isinstance(Factory, LoggerHelper):
            return Factory
        raise RuntimeError("init LoggerFactory failed!")

    def __init__(self):
        global Factory

        if Factory is None:
            try:
                with open(LOGGING_CONFIG, 'r') as f_conf:
                    dict_conf = yaml.load(f_conf)
                    logging.config.dictConfig(self.processConfigDict(dict_conf))

            except FileNotFoundError:
                try:
                    f_conf = pkgutil.get_data(__package__, LOGGING_CONFIG)
                    dict_conf = yaml.load(f_conf)
                    logging.config.dictConfig(self.processConfigDict(dict_conf))
                    if f_conf is None:
                        logging.basicConfig(level=logging.DEBUG)
                        logging.getLogger().warning('not found Logger_config')

                except Exception:
                    logging.basicConfig()
                    self.exception()

            self.DEBUGLogger.info("init LoggerFactory success!")
            self.info("init LoggerFactory success!")
        else:
            self.DEBUGLogger.warning("LoggerFactory instance is exist,  skip __init__")
            self.BaseLogger.warning('LoggerFactory instance is exist,  skip __init__')

    def processConfigDict(self, config):
        """
        替换logging的日志文件路径为绝对路径,如果解析失败返回原配置项
        :param config:
        :return:
        """
        if isinstance(config, dict):
            handlers = config.get('handlers')

            INFO = handlers.get('INFO')
            ERR = handlers.get('ERR')
            PARAMS = handlers.get('PARAMS')

            INFO['filename'] = LOGGING_JERTY
            INFO['maxBytes'] = eval(INFO['maxBytes'])
            PARAMS['filename'] = LOGGING_JERTY
            ERR['filename'] = LOGGING_ERROR

        return config

    @property
    def BaseLogger(self, name=None):
        """
        init Logger with name
        :return: RootLogger
        """
        if name:
            return logging.getLogger(name)
        return logging.getLogger()

    @property
    def DEBUGLogger(self):
        """
        use it in dev env
        :return:
        """
        return logging.getLogger('DEBUG')

    @property
    def ParamsLogger(self):
        return logging.getLogger('PARAMS')

    @property
    def ApiLogger(self):
        return logging.getLogger('API')

    def info(self, msg):
        return self.BaseLogger.info(msg)

    def error(self, msg):
        return self.BaseLogger.error(msg)

    def exception(self, msg=None):
        if msg:
            return self.BaseLogger.exception(msg)
        return self.BaseLogger.exception('捕获异常')

    @classmethod
    def log(cls, cls_):
        """
        class装饰器
        :param cls_: target class
        :return: class
        """
        cls_._logger = cls.getLoggerFactory()
        return cls_

    @staticmethod
    def exceptionDetail():
        """
        返回错误信息给调用者处理
        :return:
        """
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        err_detail = '捕获异常 In ({}, Line:{}   Method:{})    |'.format(
            filename, lineno, line.strip())
        return err_detail

    @staticmethod
    def log_params(text=None):
        """
         打印入参和结果
         :param text:str or func
         :return: log record
         """
        if isinstance(text, str):
            # 有参装饰器
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    LoggerHelper.getLoggerFactory().ParamsLogger.info(textWrapper.fill(
                        f"{func.__name__}   ---   Msg:  {text}   \nArgs: {args[1:]}\nKwargs: {kwargs}"))
                    result = func(*args, **kwargs)
                    LoggerHelper.getLoggerFactory().ParamsLogger.info(textWrapper.fill(
                        f"{func.__name__}    \n结果: {result}"))
                    return result

                return wrapper

            return decorator
        else:
            # 无参装饰器
            @wraps(text)
            def wrapper(*args, **kwargs):
                LoggerHelper.getLoggerFactory().ParamsLogger.info(textWrapper.fill(
                    f"{text.__name__}    打印入参\nArgs: {args[1:]}\nKwargs: {kwargs}"))
                result = text(*args, **kwargs)
                LoggerHelper.getLoggerFactory().ParamsLogger.info(textWrapper.fill(
                    f"{text.__name__}    \n结果: {result}"))
                return result

            return wrapper
