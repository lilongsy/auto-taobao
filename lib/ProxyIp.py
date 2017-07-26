# -*- coding: utf-8 -*-

import re
import urllib2
import json
import os
import socket
import telnetlib


class ProxyIp(object):
    def __init__(self):
        self.path = os.path.split(os.path.realpath(__file__))[0]

    # Get latest proxy ip and download to json
    def get_proxy_ips(self):
        print 'Update Ip'
        url = 'http://api.ip.data5u.com/dynamic/get.html?order=bf6d5d6ca7961a7ad5a514cbc1783cd2&random=true&sep=3'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        res = response.read().strip('\n')
        # js = json.loads(response.read().decode('gbk').encode('utf-8'))
        ips = res.split("\n");
        return ips[0]

    @staticmethod
    def is_open(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(ip, int(port))
            return True
        except:
            print 'Faild IP: %s:%s' % (ip, port)
            return False

    @staticmethod
    def is_enable(ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=20)
            return True
        except:
            return False
