#!/usr/bin/env python3
#coding:utf-8

import logging,logging.config

__author__ = 'Bambo'

log_file_path='monitoring.log'
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
      'handlers': ['info','error'],
      'level': 'INFO',
      'propagate': True
   }
 }
}

logging.config.dictConfig(LOGGING)
