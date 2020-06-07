# -*- coding: utf-8 -*-
import json
from collections import namedtuple

NetworkTuple = namedtuple('NetworkTuple', ['dev_ip', 'sip_ip'])


class NetworkMap:

    def __init__(self, dev_ip, sip_ip, device=""):
        self.dev_ip = dev_ip
        self.sip_ip = sip_ip
        self.device = device

    def __str__(self):
        s = {'dev_ip': self.dev_ip, 'sip_ip': self.sip_ip}
        if self.device:
            s['device'] = self.device
        return json.dumps(s)

    def __repr__(self):
        return self.__str__()
