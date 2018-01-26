#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import datetime

import os
import time
import redis
import traceback


def getFileName():
    t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return 'redis_log_' + t + '.log.tmp'


if __name__ == '__main__':
    #
    rootDirectory = './log/'
    # Local write redis data log file object (write a log file for every 10000 redis data)
    local_log_file = None
    # redis data list
    redis_data_list = []
    # current log file's name
    current_log_filename = ''
    # log file name list
    log_file_name_list = []

    gold_dictionary_string = ''

    try:
        # about log directory
        if os.path.exists(rootDirectory) == False:
            os.mkdir(rootDirectory)
        os.chdir(rootDirectory)

        r = redis.StrictRedis(host='115.159.144.115', port=6379, decode_responses=True, password='tvmining')
        if r.ping() == False:
            # redis connection failed, the process is over.
            exit(1)

        if len(r.keys('*')) == 0:
            exit(1)

        keys_name = r.keys('*')[0]
        while (1):
            for i in range(0, 1, 1):
                # analysis data list from redis
                redis_data_list.extend(list(eval(r.lpop(keys_name))))
            print 'redis data list length: ', len(redis_data_list)

            if len(redis_data_list) > 0:
                # print 'the first time create log file object'
                gold_dictionary_string = ''
                # get new file name by system time
                current_log_filename = getFileName()
                # open a log file object
                local_log_file = open(os.getcwd() + '/' + current_log_filename, 'w')
                # add new log filename to log file list
                log_file_name_list.append(current_log_filename)
            else:
                print 'redis data is empty'
                exit(1)

            for index, gold_dict in enumerate(redis_data_list):
                # print index, gold_dict
                if index > 0 and index % 10000 == 0:
                    # print '10 thousands. index: ', index
                    # pre log file closed
                    local_log_file.write(str(gold_dictionary_string))
                    local_log_file.flush()
                    local_log_file.close()
                    local_log_file = None
                    # print 'log file write completed.', current_log_filename

                    time.sleep(1)

                    # rename the log file
                    os.system('mv ' + current_log_filename + ' ' + os.path.splitext(current_log_filename)[0])

                    # print 'log file rename completed.', os.path.splitext(current_log_filename)[0]

                    # create a new log file for the next 10000 data
                    # print 'create a new log file.'
                    gold_dictionary_string = ''
                    current_log_filename = getFileName()
                    local_log_file = open(os.getcwd() + '/' + current_log_filename, 'w')
                    log_file_name_list.append(current_log_filename)
                else:
                    # if index % 1000 == 0:
                    #     print 'write log file, index: ', index
                    gold_dictionary_string += str(gold_dict) + '\n'

            # when the loop completed, end the log file
            local_log_file.write(str(gold_dictionary_string))
            local_log_file.flush()
            local_log_file.close()
            local_log_file = None
            # rename the log file
            os.system('mv ' + current_log_filename + ' ' + os.path.splitext(current_log_filename)[0])
            gold_dictionary_string = ''


    except Exception as ex:
        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(ex)
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
