#!/usr/bin/env python3
#coding:utf8
#coding:utf8

import logging
from ansibleapi import AnsibleApi
from config import Filer
from subprocess import Popen,PIPE


__author__ = 'Bambo'
logger = logging.getLogger('monitor')
class Server(object):
    def __init__(self,service_name,target):
        self.name = service_name
        self.target = target
        self.a = AnsibleApi()

# for init service
    def action(self,ack):
        self.task = [dict(action=dict(module='shell',args='service {0} {1}'.format(ack,self.name))),]
        data = self.a.runansible(self.target,self.task)
        logger.info('{0}\'s service: {1}  starting {2}'.format(self.target,self.name,ack))
        return data
    def start(self):
        data = self.action('start')
        return data

    def stop(self):
        data = self.action('stop')
        return data

    def restart(self):
        data = self.action('restart')
        return data

#for sv service
    def sv_action(self,ack):
        self.task = [dict(action=dict(module='shell',args="/usr/local/bin/sv {0} {1}".format(ack,self.name))),]
        data = self.a.runansible(self.target,self.task)
        logger.info('{0}\'s service: {1}  starting {2}'.format(self.target,self.name,ack))
        return data

    def sv_up(self):
        data = self.sv_action('up')
        return data

    def sv_down(self):
        data = self.sv_action('down')
        return data
#for script alert
    def runner(self,ack):
        self.task = [dict(action=dict(module='script',args="{0}".format(self.name))),]
        data = self.a.runansible(self.target,self.task)
        logger.info('{0}\'s service: {1}  starting {2}'.format(self.target,self.name,ack))
        return data
    def alert(self):
        logger.info('emiter a alert')
    def recover(self):
        logger.info('recovery a alert')

if __name__ == '__main__':
    a = Server('scavenger','10.40.39.101')
    data = a.sv_down()
    print(data)

