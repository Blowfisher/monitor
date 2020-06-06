#!/usr/bin/env python
#coding:utf8
import os
import re
import json
import yaml
import logging,logging.config
from ansibleapi import AnsibleApi


__author__ = 'Bambo'
DEFAULT_CONFIG = 'config.yml'
logger = logging.getLogger('monitor')

class Director(object):
    def __init__(self):
        pass
    def return_local_list(self,dirname):
        if os.path.exists(dirname):
            return os.listdir(dirname)
        else:
            return None
    def return_remote_list(self,target,dirname):
        # target just for single IP
        self.a = AnsibleApi()
        self.task1 = [dict(action=dict(module='shell',args='ls {0}'.format(dirname))),]
        self.task2 = [dict(action=dict(module='shell',args='[ -d {0} ] && echo True || echo False'.format(dirname))),]
        data = self.a.runansible(target,self.task2)
        if bool(json.loads(data['success'][target])['stdout_lines'][0]):
            data = self.a.runansible(target,self.task1)
            print(data)
            return json.loads(data['success'][target])['stdout_lines']
        else:
# dirname not exist
            return None


    def filter_rf(self,dirname):
        names = []
        data = dirname
        if not data: return None
        for i in data:
            name = re.match(r'^\.',i)
            if not hasattr(name,'group'):
                names.append(i)
        return names


class Filer(object):
    def __init__(self,filename):
        self.filename = filename

    def read_f(self):
        try:
            with open(self.filename,'rb') as f:
                data = f.read()
                return data
        except Exception as e:
            print('Error happened:\n {0}'.format(e))
            logginer.getLogger('monitor')
            raise Exception('Configuration file error')

    def get_yaml_data(self):
        data = yaml.load(self.read_f(),Loader=yaml.Loader)
        return data

    def dump_yaml(self,filename,obj):
        current_path = os.path.abspath('.')
        file_full_path = os.path.join(current_path,filename)
        yaml.dump(obj,file_full_path,Dumper=yaml.RoundTripDumper)
        return True

class Logger(object):
    def __init__(self,filename=DEFAULT_CONFIG):
        self.name = filename
        try:
            log_file_path = Filer(self.name).get_yaml_data()['log_file']
        except Exception as e:
            print('Configuration file\'s key:log_file is gone...')
            print('Use default log file monitoring.log')
            log_file_path = 'monitoring.log'
        LOGGING = {
'version': 1,
'disable_existing_loggers': True,
'formatters': {
   'standard': {
      'format': '%(asctime)s %(levelname)s %(message)s'
    },
   'detail':{
      'format': '%(asctime)s %(levelname)s  %(pathname)s[line:%(lineno)d] %(message)s'
   }
 },
'handlers':{
  'info':{
  'level': 'INFO',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': log_file_path,
  'maxBytes': 1024*1024*5,
  'backupCount': 3,
  'formatter': 'standard'
  },
  'warning':{
    'level': 'WARNING',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': log_file_path,
    'maxBytes': 1024*1024*5,
    'backupCount': 2,
    'formatter': 'standard'
  },
  'error':{
    'level': 'ERROR',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': log_file_path,
    'maxBytes': 1024*1024*5,
    'backupCount': 2,
    'formatter': 'detail'
  }},
'loggers':{
   'monitor':{
      'handlers': ['info',],
      'level': 'INFO',
      'propagate': True
   }
 }
}

        logging.config.dictConfig(LOGGING)


if __name__ == '__main__':
    dir_demo = Director()
    dirname = '/tmp'
    data= dir_demo.return_remote_list('10.40.39.101',dirname)

    print('The direcotry {1} has :{0}'.format(data,dirname))



