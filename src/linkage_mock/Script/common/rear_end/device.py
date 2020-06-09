# -*- coding: utf-8 -*-

PATH = '/home/fantom/apps/ngfw/local/'


def get_auth_file(name):
    """
    return auth file
    :param name: file name
    :return: dict or None
    """
    return f"{PATH}{name}"
