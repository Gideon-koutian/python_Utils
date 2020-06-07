#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, make_response, jsonify

r_AutoTest = Blueprint(__name__.split('.')[-1], __name__)
r_AutoTest.url_prefix = f"/{__name__.split('.')[-1]}"

from . import api_v1


@r_AutoTest.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), error)
