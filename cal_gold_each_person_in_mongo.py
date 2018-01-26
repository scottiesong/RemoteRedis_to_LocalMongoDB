#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
import json
import traceback
import time
import datetime
from pymongo import MongoClient


def getYestedayTimestamp():
    dt = getYestedayDateString()
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timeArray))
    return timestamp


def getYestedayDateString():
    today = datetime.datetime.now()
    yesteday = today - datetime.timedelta(days=1)
    return str(yesteday.strftime('%Y-%m-%d')) + ' 00:00:00'


if __name__ == '__main__':
    # file_log = None

    cal_standart_type = {}
    dict_type = {}
    # increase = 0
    # decrease = 0
    total = 0

    try:
        loop_index = 0
        # file_log = open('process_log.log', 'w')

        client_mongo = MongoClient('mongodb://10.0.70.31:27017', 27017)
        # flag = client_mongo.b0257617185d529c20ceffb97e82f354.authenticate('tvm', 'TvM1ning!@#', mechanism='SCRAM-SHA-1')
        flag = client_mongo.admin.authenticate('nosqluser', '654321', mechanism='SCRAM-SHA-1')
        if flag:
            print 'connect to mongodb success !'
        else:
            print 'connect to mongodb fail !'
            exit(1)
        db = client_mongo.devel

        # get all of user_info records on mongoDB
        rows = db.user_info_new1.find({}).skip(2000)

        for r in rows:
            total = 0
            ObjectId = r['_id']

            print 'id: ', ObjectId

            if r.has_key('gold'):
                # print 'has gold'

                if r['gold'].has_key('type'):
                    # print 'has type'
                    for item in range(0, len(r['gold']['type'])):
                        # current_type = r['gold']['type'][item]['type']
                        current_sum = int(r['gold']['type'][item]['sum'])
                        # calculate sum of whole type
                        total += current_sum

                    print '\ttotal sum: ', total
                else:
                    # print 'not type'
                    type_basic_json = {'type': []}
                    db.user_info_new1.update({'_id': ObjectId}, {'$set': {'gold': type_basic_json}})

                # the history list of every day gold
                if r['gold'].has_key('hist'):
                    # print 'has hist'
                    # add a group of [starttime, endtime, total] values to the array of [gold.hist]
                    db.user_info_new1.update({'_id': ObjectId},
                                             {'$push': {
                                                 'gold.hist': {'starttime': getYestedayDateString(),
                                                               'endtime': getYestedayDateString(),
                                                               'total': total}}})
                else:
                    # print 'not hist'
                    history_basic_json = {
                        'hist': [
                            {'starttime': getYestedayDateString(), 'endtime': getYestedayDateString(), 'total': total}]}
                    db.user_info_new1.update({'_id': ObjectId}, {'$set': {'gold': history_basic_json}})
                    # print json.dumps(history_basic_json, indent=4)
            else:
                # 'gold' is not exist, then add it.
                gold_basic_json = {'gold': {}}
                db.user_info_new1.update({'_id': ObjectId}, {'$set': gold_basic_json})
            loop_index += 1
            if loop_index > 1000:
                exit(1)

            # for i in dict_type.keys():
            #     total += (int(cal_standart_type[i]) * int(dict_type[i]))

            # if r.has_key('gold.hist'):
            #     r['gold.hist'].append({'starttime': '', 'endtime': 0, 'total': total})
            # else:
            #     json = {
            #         'hist': [
            #             {
            #                 'starttime': '',
            #                 'endtime': 0,
            #                 'total': total
            #             }
            #         ]
            #     }
            #     r['gold.hist'].append(json)

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
