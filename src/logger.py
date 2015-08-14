import logging
from logging.config import dictConfig


first = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
        'handlers': {
            'default': {
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter':'standard',
                },
            'persistant': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'work.log',
                'backupCount':10,
                },
            },
        'loggers': {
            '': {
                'handlers': ['default', 'persistant'],
                'level': 'DEBUG',
                'propagate': True
                },
            'bad_things': {
                'handlers': ['default'],
                'level': 'WARN',
                'propagate': False
                },
            }
        }

simple_no_file = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format':'[%(levelname)s]: %(message)s'
                },
            },
        'handlers': {
            'default': {
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter':'standard',
                },
            'persistant': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'/home/model/logs/ffeature.log',
                'backupCount':10,
                },
            },
        'loggers': {
            '': {
                'handlers': ['default', 'persistant'],
                'level': 'DEBUG',
                'propagate': True
                },
            'bad_things': {
                'handlers': ['default'],
                'level': 'WARN',
                'propagate': False
                },
            }
        }
def start_logger(id):
    if id==0:
        dictConfig(first)
    elif id==1:
        dictConfig(simple_no_file)


