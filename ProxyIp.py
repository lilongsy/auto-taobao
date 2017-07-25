# -*- coding: utf-8 -*-

import re
import urllib2
import json
import os
import socket


class ProxyIp(object):
    def __init__(self):
        self.path = os.path.split(os.path.realpath(__file__))[0]

    # Get latest proxy ip and download to json
    def get_proxy_ips(self):
        print 'Update Ip'
        url = 'http://dec.ip3366.net/api/?key=20170724181031402&getnum=30&anonymoustype=3&area=1&formats=2&proxytype=1'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return json.loads(response.read().decode('gbk').encode('utf-8'))

    @staticmethod
    def is_open(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(ip, int(port))
            return True
        except:
            print 'Faild IP: %s:%s' % (ip, port)
            return False
