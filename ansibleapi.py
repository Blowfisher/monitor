#!/usr/bin/env python3
#coding:utf8

import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
from optparse import Values
#from ansible.utils.sentinel import Sentinel


class ResultCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self,result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self,result,*args,**kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self,result,*args,**kwargs):
        self.host_ok[result._host.get_name()] = result

context.CLIARGS = ImmutableDict(connection='local',module_path=None,forks=2,become=None,become_method=None,become_user=None,check=False,diff=False)

class AnsibleApi(object):
    def __init__(self):
        self.options = {'verbosity' : 0,'ask_pass': False,'private_key_file': None,'remote_user':None,'connection': 'smart','timeout': 10,'ssh_common_args': '','flush_cache': True,'inventory': '/etc/ansible/hosts','fork': 1,'args': ['fake']}
        self.ops = Values(self.options)
        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=[self.options['inventory']])
        self.variable_manager = VariableManager(loader=self.loader,inventory=self.inventory)

    def runansible(self,host_list,task_list):
        play_source = dict(
               name = "Ansible play",
               hosts = host_list,
               gather_facts = 'no',
               tasks = task_list
)
        play = Play().load(play_source,variable_manager=self.variable_manager,loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                   inventory = self.inventory,
                   variable_manager = self.variable_manager,
                   loader = self.loader,
                   passwords = self.passwords,
                   stdout_callback = self.results_callback,
                   run_additional_callbacks = C.DEFAULT_LOAD_CALLBACK_PLUGINS,
#                   fun_tree = False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                 tqm.cleanup()
                 shutil.rmtree(C.DEFAULT_LOCAL_TMP,True)
        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreacheable'] = {}

        for host,result in self.results_callback.host_ok.items():
            results_raw['success'][host] =  json.dumps(result._result)

        for host,result in self.results_callback.host_failed.items():
            results_raw['failed'][host] =  result._result['msg']

        for host,result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] =  result._result['msg']

        return results_raw

    def playbookrun(self,playbook_path):
        context._init_global_context(self.ops)
        playbook = PlaybookExecutor(playbook=playbook_path,inventory=self.inventory,variable_manager=self.variable_manager,loader=self.loader,passwords=self.passwords)
        result = playbook.run()
        return result


if __name__ == '__main__':
    a = AnsibleApi()
    host_list = '10.40.39.101'
    dirname = '/tmp'
    tasks_list = [dict(action=dict(module='command',args='ls {0}'.format(dirname))),]
    data = a.runansible(host_list,tasks_list)
    print(json.loads(data['success']['10.'])['stdout_lines'])
                                                            
