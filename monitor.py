#!/usr/bin/benc python3
#coding:utf8

import os
import time
import json
import random
import yaml
import logging
from datetime import datetime
from test.ansibleapi import AnsibleApi
from test.dirname import Director,Filer
from test.server  import Server

class Monitor(object):
    def __init__(self,timer,filename):
        self.timer = timer
        self.timer_list = sort(list(timer))
        self.sleep_time = 300
        self.filename = filename

        while True:
#立即发出告警
            if os.path.exist(filename) and old_mtime == os.path.getmtime(filename):
                time.sleep(30)
            else:
                old_mtime == os.path.getmtime(filename)


            if fier_guarder is emiter:
                service = Server(servername,target)
                data = service.sv_down()
                logger.info(data)
#正常告警
            else:
                now_hour = datetime.now().hour
                if now_hour == self.timer_list[0]:
                    service = Server(servicename,target)
                    data = service.sv_down()
                    logger.info(data)
                    time.sleep(self.sleep_time)
                    data = service.sv_up()
                    logger.info(data)
                    self.timer_list.pop(0)
            time.sleep(30)
