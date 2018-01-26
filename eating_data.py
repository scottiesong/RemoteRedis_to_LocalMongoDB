#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import time

import datetime
import redis
import traceback

if __name__ == '__main__':
    current_data_count = 0
    try:
        r = redis.StrictRedis(host='115.159.144.115', port=6379, decode_responses=True, password='tvmining')
        redis_data_list = []

        while (1):
            try:
                # r.lpop(r.keys('*')[0])
                redis_data_list = list(eval(r.lpop(r.keys('*')[0])))

                current_data_count += len(redis_data_list)
            except Exception as ex:
                time.sleep(60)
                if current_data_count > 0:
                    print datetime.datetime.now(), '\t', current_data_count

                current_data_count = 0
                redis_data_list = []

                continue
    except Exception as e:

        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(e)
        print '\ttraceback.format_exc():\n%s' % traceback.format_exc()
    finally:
        print 'process is over.'
