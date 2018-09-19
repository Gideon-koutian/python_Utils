#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
from posixpath import normpath
import requests
import json

from src.diy_logging.logginghelper import LoggerHelper

sessionFactory = None


def url_Join(base: str, url: str) -> str:
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))


def cmp(expect_data, actual_data, curent_key, assert_result, assert_pass):
    if isinstance(actual_data, dict):
        """dict"""
        for expect_key in expect_data.keys():
            if expect_key in actual_data:
                actual_value = actual_data[expect_key]
                expect_value = expect_data[expect_key]
                cmp(expect_value, actual_value,
                    expect_key, assert_result, assert_pass)
            else:
                assert_pass["assert_pass"] = False
                assert_result.append(
                    {expect_key: "Expect find key ['" + expect_key + "'],but not found the key"})

    elif isinstance(actual_data, list):
        """list"""
        for expect in expect_data:
            if not expect in actual_data:
                assert_pass["assert_pass"] = False
                assert_result.append(
                    {curent_key: "Expect find ['" + str(expect_data) + "'],but found " + str(
                        actual_data)})
                # cmp(expect_data, actual_data, curent_key, assert_result)

    else:
        if str(expect_data) != str(actual_data):
            assert_pass["assert_pass"] = False
            assert_result.append(
                {curent_key: "Expect find ['" + str(expect_data) + "'],but found " + str(actual_data)})

    return assert_pass, assert_result


@LoggerHelper.log
class RequestUtil:
    _req = None

    @staticmethod
    def set_session(session=None):
        global sessionFactory
        if session:
            sessionFactory = session
        else:
            sessionFactory = requests.session()

    @staticmethod
    def release_session():
        global sessionFactory
        sessionFactory = None

    def check_session(self):
        global sessionFactory
        if sessionFactory is None:
            self.set_session()

    def handel_headers(self, headers):
        try:
            _header = json.loads(headers, encoding='utf-8')
        except:
            if isinstance(headers, (str, bytes)) and headers.startswith('{') and headers.endswith(
                    '}'):
                _header = json.loads(headers, encoding='utf-8')
                _keys = list(map(lambda x: x.upper(), _header.keys()))
                if 'content-type'.upper() not in _keys:
                    _header['Content-Type'] = 'application/json; charset=utf-8'
                return _header
            elif isinstance(headers, dict):
                _keys = list(map(lambda x: x.upper(), headers.keys()))
                if 'content-type'.upper() not in _keys:
                    headers['Content-Type'] = 'application/json; charset=utf-8'
                return headers
            else:
                if headers:
                    raise ValueError("请求头必须是JSON格式")
                else:
                    return {'Content-Type': 'application/json; charset=utf-8'}
        else:
            _keys = list(map(lambda x: x.upper(), _header.keys()))
            if 'content-type'.upper() not in _keys:
                _header['Content-Type'] = 'application/json; charset=utf-8'
            return _header

    def handel_cookie(self, session=None):
        global sessionFactory
        _cookiestr = ""

        # for cookie in session.cookies:
        for _cookie in sessionFactory.cookies:
            temp = _cookie.name + '=' + _cookie.value + ';'
            _cookiestr += temp
        return _cookiestr

    def handel_kwargs(self, kwargs: dict):
        """
        set default timeout = 30
        """
        if 'timeout' in kwargs:
            pass
        else:
            kwargs['timeout'] = 30

        return kwargs

    @classmethod
    def request(cls, method: str, request_url: str, **kwargs):
        _input_param = kwargs.pop('input_param', None)
        _headers = kwargs.pop('headers', None)
        _session = kwargs.pop('session', False)

        _headers = cls().handel_headers(_headers)
        # default type
        input_type = 'data'

        if _session:
            cls().check_session()
            cls._req = sessionFactory
            _cookie = cls().handel_cookie()
            # cls._req = session
            # cookie = cls().handel_cookie(session)
            if _cookie != "":
                if 'Cookie'.upper() in list(map(lambda x: x.upper(), _headers.keys())):
                    pass
                else:
                    _headers['cookie'] = _cookie

        else:
            cls._req = requests

        _data = {}
        if _input_param:

            if "GET" == method.upper():
                input_type = 'params'

            elif "POST" == method.upper():
                if isinstance(_input_param, dict):
                    input_type = 'json'
                else:
                    pass
            else:
                pass

        _data[input_type] = _input_param

        kwargs = dict(_data, **cls().handel_kwargs(kwargs))
        # cls._logger.DEBUGLogger.info(f"请求:   {method.upper()} {request_url} {headers} {kwargs}")
        cls._logger.info(f"请求:  {method.upper()}    {request_url}     {_headers}      {kwargs}")

        return cls._req.request(method.upper(), request_url, headers=_headers, **kwargs)


if __name__ == "__main__":
    res = RequestUtil.request('get', 'https://www.baidu.com',
                              headers=json.dumps({"Content-Type": "application/x-www-form-urlencoded"},
                                                 ensure_ascii=False),
                              input_param="username=lanlan&password=111111&appid=86193301644464128")
    print(res.text)
