# -*- coding: UTF-8 -*-
import platform

# redis log server
SRC_SERVER_IP = ''
SRC_SERVER_USERNAME = ''
SRC_SERVER_PASSWORD = ''
SRC_SERVER_WORK_DIRECTORY_FULL_PATH = ''

# local log directory path
LOCAL_LOG_PATH = './log/'

# md5 file name
MD5_FILE = 'md5_set'


def getSystemType():
    # return the type of system
    return platform.system()
