#!/usr/bin/env python3
#coding:utf8

import random
import time
from datetime import datetime,timedelta



class Timer(object):
    def __init__(self,times,start_point,end_point):
        self.times = times
        self.time_set = (start_point,end_point)

    def generator(self):
        data = []
        for i in range(self.times):
            data.append(random.randint(self.time_set[0],self.time_set[1]))
            time.sleep(1)
        return sorted(data)
    @classmethod
    def local_now_timer(cls):
        dt = (datetime.now()+timedelta(hours=8)).ctime().replace("'",'')
        return dt

if __name__ == '__main__':
    a = Timer.local_now_timer()
    print(a)
