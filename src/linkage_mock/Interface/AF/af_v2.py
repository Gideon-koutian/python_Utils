#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import r_AF


@r_AF.route("/v2/get_all_apps")
def get_all_apps_v2():
    pass


@r_AF.route("/v2/get_apps_by_page")
def get_apps_byPage_v2():
    pass


@r_AF.route("/v2/add_app", methods=['post'])
def add_app_v2():
    pass


@r_AF.route("/v2/edit_app/v2/<app_id>", methods=['post'])
def edit_app_v2(app_id):
    pass


@r_AF.route("/v2/delete_app/v2/<app_id>", methods=['delete'])
def delete_app_v2(app_id):
    pass
