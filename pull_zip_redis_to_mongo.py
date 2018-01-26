#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import os
import time
import threading
import traceback
import config


def get_MD5_zip_packs(zipPath):
    current_md5 = None
    if systemType == 'Darwin':
        current_md5 = str(os.popen('md5 ' + zipPath).read().split()[3])
    elif systemType == 'Linux':
        current_md5 = str(os.popen('md5sum ' + zipPath).read().split()[0])
    elif systemType == 'Windows':
        current_md5 = ''
    else:
        current_md5 = None
    return current_md5


def read_MD5_list(path, filename):
    try:
        global md5_dictionary
        for line in open(path + filename):
            md5_dictionary = eval(line)

    except Exception as ex:
        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(ex)
        print '\ttraceback.format_exc():\n%s' % traceback.format_exc()


def pull_single_zip_pack_retry_3_times(zipName, local_log_directory):
    # pull a zip pack by zip pack name
    pull_command_line = 'sshpass -p ' + config.SRC_SERVER_PASSWORD + \
                        ' scp ' + config.SRC_SERVER_USERNAME + '@' + config.SRC_SERVER_IP + ':' + \
                        config.SRC_SERVER_WORK_DIRECTORY_FULL_PATH + '/' + zipName + ' ' + \
                        local_log_directory

    for i in range(0, 4, 1):
        r = os.system(pull_command_line)
        if r != 0:
            continue
        else:
            return True
    return False


def pull_zip_packs_to_local_log(local_log_directory):
    src_ip = config.SRC_SERVER_IP
    src_usr = config.SRC_SERVER_USERNAME
    src_pwd = config.SRC_SERVER_PASSWORD
    src_root_directory = config.SRC_SERVER_WORK_DIRECTORY_FULL_PATH

    pull_md5_file_cmd_line = 'sshpass -p ' + src_pwd + \
                             ' scp ' + src_usr + '@' + src_ip + ':' + src_root_directory + '/' + config.MD5_FILE + ' ' + \
                             local_log_directory

    r = os.system(pull_md5_file_cmd_line)
    if r != 0:
        print 'pull failed'
        return
    else:
        # pull success, and pull whole the zip packs
        pull_command_line = 'sshpass -p ' + src_pwd + \
                            ' scp ' + src_usr + '@' + src_ip + ':' + src_root_directory + '/*.tar.gz ' + \
                            local_log_directory

        r = os.system(pull_command_line)
        if r != 0:
            print 'pull zip packs failed'
            return
        else:
            print 'pull zip success'
    # while (1):
    #     print 'pull_zip_packs_to_local_log'
    #     time.sleep(1)


def unzip_packs_to_log_directory(local_log_directory):
    # read log file to dictionary
    for parent, dirnames, filenames in os.walk(local_log_directory):
        # 输出文件信息
        for filename in filenames:
            ext_name = os.path.splitext(os.path.splitext(filename)[0])[1] + os.path.splitext(filename)[1]
            if ext_name == '.tar.gz':

                md5_value = md5_dictionary[filename]

                # command success, and unzip all zip packs
                unzip_command_line = 'tar -xzf ' + filename + ' -C ' + local_log_directory
                r = os.system(unzip_command_line)
                if r != 0:
                    # retry unzip 3 times
                    for i in range(0, 4, 1):
                        r = os.system(unzip_command_line)
                        if r != 0:
                            continue
                        else:
                            break

                # delete zip file
                os.system('rm -rf ' + filename)
    # while (1):
    #     print 'unzip_packs_to_log_directory'
    #     time.sleep(1.5)


class pull_thread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.args = args

    def run(self):
        while (True):
            pull_zip_packs_to_local_log(self.args)
            time.sleep(1)


class unzip_thread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.args = args

    def run(self):
        while (True):
            unzip_packs_to_log_directory(self.args)
            time.sleep(1)


if __name__ == '__main__':
    try:
        global systemType
        systemType = config.getSystemType()

        # local_log_directory = config.LOCAL_LOG_PATH
        #
        # p = pull_thread(args=local_log_directory)
        # u = unzip_thread(args=local_log_directory)
        #
        # p.start()
        # u.start()

        read_MD5_list('./log/tar/', 'md5_set')

        for i in md5_dictionary:
            print i, md5_dictionary[i]

    except Exception as e:

        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(e)
        print '\ttraceback.format_exc():\n%s' % traceback.format_exc()

        # file_log.write('Exception: \n')
        # file_log.write('\tException Description:\t' + str(Exception) + '\n')
        # file_log.write('\tError message:\t\t' + str(e) + '\n')
        # file_log.write('\ttraceback.format_exc():\n%s' % traceback.format_exc() + '\n')
        # file_log.flush()
    finally:
        print 'process is over.'
        # file_log = open('process_log.log', 'a')
        # file_log.write('=======================================================\n')
        # file_log.write('=======================================================\n\n')
        # file_log.flush()
        # file_log.close()
