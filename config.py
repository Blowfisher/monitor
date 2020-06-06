#!/usr/bin/env python
#coding:utf8
import os
import re
import json
import yaml
from ansibleapi import AnsibleApi


__author__ = 'Bambo'

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
        with open(self.filename,'rb') as f:
            data = f.read()
            return data

    def get_yaml_data(self):
        data = yaml.load(self.read_f(),Loader=yaml.Loader)
        return data

    def dump_yaml(self,filename,obj):
        current_path = os.path.abspath('.')
        file_full_path = os.path.join(current_path,filename)
        yaml.dump(obj,file_full_path,Dumper=yaml.RoundTripDumper)
        return True



if __name__ == '__main__':
    dir_demo = Director()
    dirname = '/tmp'
    data= dir_demo.return_remote_list('10.40.39.101',dirname)

    print('The direcotry {1} has :{0}'.format(data,dirname))



