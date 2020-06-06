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
from ansible.utils.sentinel import Sentinel


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

#context.CLIARGS = ImmutableDict(connection='local',module_path=None,forks=2,become=None,become_method=None,become_user=None,check=False,diff=False)
context.CLIARGS = ImmutableDict(connection='smart', module_path=None, verbosity=5,forks=1, become=None, become_method=None,become_user=None, check=False, diff=False)

class AnsibleApi(object):
    def __init__(self):
        self.options ={'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': None,
                    'connection': 'smart', 'timeout': 10, 'ssh_common_args': '', 'sftp_extra_args': '',
                    'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
                    'become': False, 'become_method': 'sudo', 'become_user': None, 'become_ask_pass': False,
                    'tags': ['all'], 'skip_tags': [], 'check': False, 'syntax': None, 'diff': False,
                    'inventory': '/etc/ansible/hosts',
                    'listhosts': None, 'subset': None, 'extra_vars': [], 'ask_vault_pass': False,
                    'vault_password_files': [], 'vault_ids': [], 'forks': 5, 'module_path': None, 'listtasks': None,
                    'listtags': None, 'step': None, 'start_at_task': None, 'args': ['fake']}
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
                   run_tree = False,
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
    host_list = ['192.168.16.105',]
#    dirname = '/tmp'
    tasks_list = [dict(action=dict(module='command',args="ls /tmp"))]
    data = a.runansible(host_list,tasks_list)
    print(data['success']['192.168.16.105'])
                                                            
