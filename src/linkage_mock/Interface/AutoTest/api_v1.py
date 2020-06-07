#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify, request, json, g

from . import r_AutoTest


@r_AutoTest.route('/devices')
@r_AutoTest.route('/devices/<string:_type>')
def devices(_type=None):
    return make_response(jsonify({"success": True, "data": g.ip_pool.devices(_type)}), 200)


@r_AutoTest.route('/distribution_ip', methods=["GET", 'POST'])
def distribution_network_ip():
    """
    根据请求来源进行分配虚拟设备IP
    :return:
    """
    _DEV = 'Virtual_device'
    _SIP = 'SIP_device'
    _TYPE_MAP = {
        _DEV: 'dev_ip',
        _SIP: 'sip_ip'
    }

    if 'POST' == request.method:
        args = request.args.to_dict()
    else:
        args = request.json

    ip, type, device = args.get('ip', None), args.get('type', None), args.get('device', None)
    if not (ip and type and device):
        return make_response(jsonify({"success": False, "msg": f"params:{args} is illegal"}), 200)

    if type not in _TYPE_MAP:
        return make_response(jsonify({"success": False, "msg": f"ip type:{type} not in {_TYPE_MAP.keys()}"}), 200)

    success, result = g.ip_pool.generate(device, **{_TYPE_MAP[type]: ip})
    return make_response(jsonify({"success": success, "result": result}), 200)