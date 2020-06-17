#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, make_response, jsonify

r_EDR = Blueprint(__name__.split('.')[-1], __name__)
r_EDR.url_prefix = f"/actual_{__name__.split('.')[-1]}"
_PORT = 7443

from . import edr_v1


@r_EDR.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), error)
