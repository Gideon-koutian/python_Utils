# -*- coding: utf-8 -*-
import logging as _logging
import sys

from flask import *
from loguru import logger
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import find_modules, import_string

import Tools.Others.ip_pool as ip_pool

APP = Flask(__name__)
APP.wsgi_app = ProxyFix(APP.wsgi_app)
logger.add(sink=sys.stdout, level=_logging.ERROR, backtrace=True, catch=True)
Logger = logger.bind(WEB=True)
WHITE_LIST = ['AutoTest', 'actual_']


@APP.before_request
def before_request():
    """
    1.判断请求IP是否以及接入 Y=》5  N=》2
    2.模拟设备认证
    3.设备接入（单向、双向） -  分配对应虚拟设备IP，存储字典
    4.发送心跳  -   定时心跳（默认持续时长1hour，支持拓展）
    5.模拟信息同步
    6.模拟对应联动接口
    7.设备断开接入    -   释放分配的虚拟设备IP，字典存储
    :return:
    """
    g.local_ip = request.host.split(':')[0]
    g.request_ip = request.remote_addr
    g.request_port = request.environ.get("SERVER_PORT", 0)
    g.interface = request.path

    g.ip_pool = ip_pool

    global WHITE_LIST
    for w in WHITE_LIST:
        if w in g.interface:
            # 全局白名单
            Logger.info(f"interface:{g.interface} in WHITE_LIST.passed")
            return None
    """
        先判断请求IP是否接入，直接redirect转发endpoint
        再判断url对应哪种设备，再redirect到对应route
            重复场景暂不支持
    """
    rules = [r for r in APP.url_map.iter_rules() if g.interface in r.rule]

    if len(rules) != 1:
        return make_response(
            jsonify({"success": False, "msg": f"{g.interface} match one more interface rules" if len(
                rules) else f"interface:{g.interface} no exist"}), 500)
    rule = rules[0]
    device_type = rule.endpoint.split('.')[0]

    if not ip_pool.is_access():
        Logger.info(f"({g.request_ip}->{g.local_ip}) is not access.try to access")

        try:
            # 分配对应虚拟设备IP，存储字典
            ip_pool.update_DeviceMap(device_type)
            return ip_pool.proxy(url_for(rule.endpoint, _external=True))

        except Exception as e:
            Logger.exception(_Logger__message=e)
            ip_pool.del_DeviceMap()
            return make_response(jsonify({"success": False, "msg": f"happen Exception", "detail": repr(e)}), 501)
    else:
        Logger.info(f"({g.request_ip}->{g.local_ip}) is accessed.try to redirect")
        exist_device_type = ip_pool.DeviceMap_val()

        if device_type != exist_device_type:
            return make_response(jsonify(
                {"success": False,
                 "msg": f"platform has distribution ip:{g.local_ip} for a {exist_device_type} device for SIP:{g.request_ip}."
                 f"no support to request interface of other device: {device_type}"}),
                501)
        return ip_pool.proxy(url_for(rule.endpoint, _external=True))


# 允许跨域访问
@APP.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Access-Token")
    response.headers.add("Access-Control-Expose-Headers", "*")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    response.headers.add('Access-Control-Allow-Methods', '*')

    # 根据需求更改返回json以及status_code

    return response


def load_web():
    for name in find_modules('Interface', include_packages=True):
        APP.register_blueprint(getattr(import_string(name), f"r_{name.split('.')[-1]}", None))


def main():
    # print(APP.url_map)
    APP.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port='7443')


if __name__ == '__main__':
    """
        模拟sangfor设备接入/联动/同步信息
        支持设备认证、心跳
        联动策略下发（成功、失败）
        资产、在线用户信息同步（支持mock）
    """
    load_web()
    main()
