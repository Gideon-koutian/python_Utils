# -*- coding: utf-8 -*-
import logging as _logging
import sys
import getopt

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
    _replace = ip_pool.has_diy_return(g.request_ip, g.local_ip, g.interface)
    if _replace[0]:
        status_code = _replace[1].get('status_code', None)
        headers = _replace[1].get('headers', {})
        data = _replace[1].get('data', {})

        response.status_code = status_code if status_code else response.status_code

        if headers:
            for k in headers:
                response.headers[k] = headers[k]

        _replace_type = data.pop('_replace_type', 'all')
        if _replace_type not in ['all', 'replace']:
            _replace_type = 'all'

        if 'all' == _replace_type:
            response.set_data(json.dumps(data))
        else:
            for d in data:
                response.json[d] = data[d]

    return response


def __load_web(port: int):
    """
    load blueprint
    :param port:
    :return:
    """
    for name in find_modules('Interface', include_packages=True):
        _module = import_string(name)
        if 'AutoTest' in name or int(port) == getattr(_module, '_PORT', None):
            APP.register_blueprint(getattr(_module, f"r_{name.split('.')[-1]}", None))


def __app(port=7443):
    print(APP.url_map)
    APP.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=port)


def run(port):
    _p = int(port)

    if not (0 < _p <= 65535):
        raise RuntimeError("invaild port range")
    __load_web(_p)
    __app(_p)


if __name__ == '__main__':
    """
        模拟sangfor设备接入/联动/同步信息
        支持设备认证、心跳
        联动策略下发（成功、失败）
        资产、在线用户信息同步（支持mock）
    """
    port = None
    opts, args = getopt.getopt(sys.argv[1:], '-h-p:', ['help', 'port='])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
            sys.exit(0)
        elif opt_name in ('-p', '--port'):
            port = int(opt_value)

    if not port:
        print("PARAM: port is must")
        sys.exit(-1)

    __load_web(port)
    __app(port)
