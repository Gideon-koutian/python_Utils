#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, make_response, jsonify

r_AF = Blueprint(__name__.split('.')[-1], __name__)
r_AF.url_prefix = f"/actual_{__name__.split('.')[-1]}"

from . import af_v1
from . import af_v2


@r_AF.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), error)
