# -*- coding: utf-8 -*-

from Script.common.rear_end.device import *


class Operaction:
    _auth_file = 'af_manager.json'
    _device_type = 'AF'

    @classmethod
    def is_access(cls):
        # 检查前台接入记录
        # 检查后台配置文件
        if not get_auth_file(cls._auth_file):
            return False
        else:
            pass
        return True

    @classmethod
    def device_record(cls):
        return None
