#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify, request
from . import r_AF


@r_AF.route("/v1/get_all_apps2")
def get_all_apps_v1():
    print("test af success")
    return make_response(jsonify({"success": True, "msg": "test af ok"}), 200)


@r_AF.route("/v1/test")
def test():
    print("test success")
    return make_response(jsonify({"success": True, "msg": "test ok"}), 200)


@r_AF.route("/v1/add_app", methods=['post'])
def add_app_v1():
    pass


@r_AF.route("/v1/edit_apps/v1/<app_id>", methods=['post'])
def edit_app_v1(app_id):
    pass


@r_AF.route("/v1/delete_apps/v1/<app_id>", methods=['delete'])
def delete_app_v1(app_id):
    pass
