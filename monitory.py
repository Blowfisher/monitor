#!/usr/bin/benc python3
#coding:utf8

import os
import time
import json
import log_helper
import logging
from datetime import datetime
from ansibleapi import AnsibleApi
from config import Director,Filer
from timer import Timer
from server  import Server,Emitor

log_file_path='monitoring.log'
logger = logging.getLogger('monitor')

class Monitor(object):
    mtime = float()
    logger.info('mtime is {0}'.format(mtime))
    def __init__(self,filename):
        if os.path.exists(filename):
            self.filename = filename
            self.__reload()
        else:
            raise('{0} not exists.'.format(filename))

    def __reload(self):
        self.config = Filer(self.filename).get_yaml_data()
        self.times = self.config['times']
        self.intervals = self.config['intervals']
        self.start_point = self.config['time_zone']['start_point']
        self.end_point = self.config['time_zone']['end_point']
        self.scripts = self.config['scripts']
        self.actions = self.config['actions']

    def start(self):
        logger.info('Monitor Emiter starting')
        self.timer_list = Timer(self.times,self.start_point,self.end_point).generator()
        logger.info('Today emiter time is: {0}'.format(self.timer_list))
        while True:
            if Monitor.mtime == os.path.getmtime(self.filename):
                logger.info('{0} mtime {1} is not changed Check time...'.format(self.filename,Monitor.mtime))
                self.check()
            else:
                Monitor.mtime = os.path.getmtime(self.filename)
                logger.info('{0} has changed...'.format(self.filename))
                logger.info('Reload {0} ...'.format(self.filename))
                logger.info('mtime is {0}'.format(Monitor.mtime))
                self.__reload()
            time.sleep(self.intervals)
    def check(self):
        if datetime.now().hour >  self.timer_list[0]:
            self.timer_list.pop(0)
        if len(self.timer_list) <= 0 and datetime.now().hour <= 1:
            self.timer_list = Timer(self.times,self.start_point,self.end_point).generator()
        if datetime.now().hour == self.timer_list[0]:
            pass
            num = self.timer_list.pop(0)
            logger.info('{0} task start...'.format(num))

if __name__ == '__main__':
    a = Monitor('config.yml')
    a.start()

