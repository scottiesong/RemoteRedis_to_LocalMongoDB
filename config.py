# -*- coding: UTF-8 -*-
import os
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


def get_MD5_zip_packs(zipPath):
    current_md5 = None
    systemType = getSystemType()
    if systemType == 'Darwin':
        current_md5 = str(os.popen('md5 ' + zipPath).read().split()[3])
    elif systemType == 'Linux':
        current_md5 = str(os.popen('md5sum ' + zipPath).read().split()[0])
    # elif systemType == 'Windows':
    #     current_md5 = ''
    else:
        current_md5 = ''
    return current_md5
