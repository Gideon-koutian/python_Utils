# -*- coding: utf-8 -*-

from flask import g, request, make_response, jsonify, Response, current_app
import requests
import socket
from requests_toolbelt.adapters import SourceAddressAdapter
from Tools.Models.data_models import NetworkMap

DeviceMap = {}


# 操作加锁

def generate(device_type, dev_ip=None, sip_ip=None):
    if not (dev_ip and sip_ip):
        return False, 'dev_ip or sip_ip must need one'
    return True, '1.1.1.1'


def is_access():
    key = (g.local_ip, g.request_ip)
    return key in DeviceMap


def DeviceMap_val():
    key = (g.local_ip, g.request_ip)
    return DeviceMap.get(key, None)


def update_DeviceMap(val):
    key = (g.local_ip, g.request_ip)
    DeviceMap[key] = val


def del_DeviceMap():
    key = (g.local_ip, g.request_ip)
    del DeviceMap[key]


def devices(_type):
    return [NetworkMap(*k, device=v) for k, v in DeviceMap.items() if v == _type] if _type else [
        NetworkMap(*k, device=v) for k, v in DeviceMap.items()]


def handel_request(dev_ip):
    """
    负责虚拟设备主动接入请求用
    :param dev_ip: 虚拟设备ip
    :return:
    """
    s = requests.Session()
    s.mount('http://', SourceAddressAdapter(dev_ip))
    s.mount('https://', SourceAddressAdapter(dev_ip))
    return requests.Session()


# def handel_request(src_ip, target_ip, target_port, data):
#     # with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as _sock:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _sock:
#         _sock.bind((src_ip, 0))
#         _sock.listen(1)
#
#         sock = ssl.wrap_socket(_sock)
#
#         if type(data) in [dict, list]:
#             _data = json.dumps(data)
#         else:
#             _data = str(data)
#
#         sock.connect((target_ip, target_port))
#         sock.sendall(_data)
#         # sock.sendto(data, (target_ip, target_port))
#         _response = sock.recv(8192)
#         # sock.recvfrom(8192)
#         response = json.loads(_response)
#         print(response)

def proxy(url, *args, **kwargs):
    body = {"url": url, "method": request.method, "verify": False,
            "headers": {key: value for (key, value) in request.headers}, "cookies": request.cookies,
            "allow_redirects": False}

    if len(request.args):
        body['params'] = request.args

    if request.is_json:
        body['json'] = request.json
    elif len(request.form):
        body['data'] = request.form
    else:
        body['data'] = request.get_data()

    if request.files:
        return make_response(jsonify({"scuuess": False, "msg": "暂不支持文件类型数据转发"}), 500)

    resp = requests.request(**body)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


def get_host_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        print("getsockname", s.getsockname())
        ip = s.getsockname()[0]
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for addr in addrs:
            print(addr)
        print(ip)


if __name__ == '__main__':
    get_host_ip()
