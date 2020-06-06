#!/usr/bin/benc python3
#coding:utf8

import os
import sys
import time
import json
import logging
from datetime import datetime
from subprocess import Popen,PIPE
from ansibleapi import AnsibleApi
from config import Director,Filer,Logger
from timer import Timer
from server  import Server

logger = logging.getLogger('monitor')

class Emitor(object):
    mtime = float()
    try:
        common = str(Popen("a=`ansible all --list-hosts|tr -d ' '`&& echo $a",shell=True,stdout=PIPE,stderr=PIPE).stdout.read()).strip('\\n\'\"').split(' ')[1:]
    except Exception as e:
        print('Error happend:\n {0}'.format(e))
        logger.error('Error happend:\n {0}'.format(e))
        sys.exit(1)
    def __init__(self,filename):
        if os.path.exists(filename):
            self.num = None
            self.times = None
            self.timer_list = None
            self.filename = filename
            self.__reload()
        else:
            raise('{0} not exists.'.format(filename))
    @classmethod
    def emiter_com(cls):
        """return common ip"""
        return Emitor.common[random.randint(0,len(Emitor.common)-1)]
    @classmethod
    def emiter_spec(cls,servicename):
        """return specific service\'s ip"""
        spec = str(Popen("a=`ansible {0} --list-hosts|tr -d ' '`&& echo $a".format(servicename),shell=True,stdout=PIPE,stderr=PIPE).stdout.read()).strip('\\n\'\"').split(' ')[1:]
        return spec[random.randint(0,len(spec)-1)]

    def __reload(self):
        self.config = Filer(self.filename).get_yaml_data()
        self.intervals = self.config['intervals']
        self.start_point = self.config['time_zone']['start_point']
        self.end_point = self.config['time_zone']['end_point']
        self.items = self.config['items']
        self.service = self.config['services']
        self.scripts = self.config['scripts']
        self.actions = self.config['actions']
        self.log_file = self.config['log_file']
        if self.times != self.config['times']:
            self.times = self.config['times']
            self.timer_list = Timer(self.times,self.start_point,self.end_point).generator()
            logger.info('New emiter time is: {0}'.format(self.timer_list))

    def start(self):
        logger.info('Monitor Emiter starting')
        Emitor.mtime = os.path.getmtime(self.filename)
        logger.info('{0} file\'s mtime is {1}'.format(self.filename,Emitor.mtime))
        while True:
            if Emitor.mtime != os.path.getmtime(self.filename):
                Emitor.mtime = os.path.getmtime(self.filename)
                logger.info('configuration file:{0} has changed...'.format(self.filename))
                logger.info('Reload {0} ...'.format(self.filename))
                logger.info('mtime is {0}'.format(Emitor.mtime))
                self.__reload()
            self.check()
            time.sleep(self.intervals)

    def check(self):
        if len(self.timer_list) <= 0 and datetime.now().hour <= 1:
            if self.times == 0:
                return 
            self.timer_list = Timer(self.times,self.start_point,self.end_point).generator()
            logger.info('generator a  new alert plan...')
            logger.info('New emiter time is: {0}'.format(self.timer_list))
        if len(self.timer_list) == 0:
            return 
        if datetime.now().hour == self.timer_list[0]:
            self.num = self.timer_list.pop(0)
            logger.info('{0} task start...'.format(self.num))
        if datetime.now().hour >  self.timer_list[0]:
            self.timer_list.pop(0)
            logger.info('Poped one pointer...')

if __name__ == '__main__':
    Logger()
    a = Emitor('config.yml')
    a.start()
