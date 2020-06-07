#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify, request, json

from . import r_EDR


@r_EDR.route("/v1/get_all_apps1")
def get_all_apps_v1():
    print("success")
    return make_response(jsonify({"success": True, "msg": "get_all_apps_v1 ok"}), 200)


@r_EDR.route("/v1/get_apps_by_page1")
def get_apps_byPage_v1():
    args = request.args.to_dict()
    print(f"params：{args}")
    return make_response(jsonify({"success": True, "msg": "get_apps_by_page1 ok"}), 200)


@r_EDR.route("/v2/test")
def test():
    print("test success")
    return make_response(jsonify({"success": True, "msg": "test EDR ok"}), 200)


@r_EDR.route("/v1/edit_app/<tocken>", methods=['post'])
def edit_app_v1(tocken):
    data = request.json
    print(f"data:{data}")
    return make_response(jsonify({"success": True, "msg": "test EDR edit_app_v1 ok"}), 200)


@r_EDR.route("/v1/delete_EDR_app", methods=['post'])
def delete_app_v1():
    args = request.args.to_dict()
    data = request.json
    print(f"args：{args}, data:{data}")
    return make_response(jsonify({"success": True, "msg": "test EDR delete_app_v1 ok"}), 200)
