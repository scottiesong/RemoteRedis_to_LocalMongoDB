#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import os
import time
import traceback
import datetime
from pymongo import MongoClient

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    type_list = []

    try:
        loop_index = 0
        client_mongo = MongoClient('mongodb://10.0.70.31:27017', 27017)
        # flag = client_mongo.b0257617185d529c20ceffb97e82f354.authenticate('tvm', 'TvM1ning!@#', mechanism='SCRAM-SHA-1')
        flag = client_mongo.admin.authenticate('nosqluser', '654321', mechanism='SCRAM-SHA-1')
        if flag:
            print 'connect to mongodb success !'
        else:
            print 'connect to mongodb fail !'
            exit(1)
        db = client_mongo.devel
        is_first = True
        # read log file to dictionary
        for parent, dirnames, filenames in os.walk('./log/'):
            # 输出文件信息
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.log':
                    if is_first:
                        is_first = False
                        continue
                    for line in open(parent + filename):
                        current_dict = eval(line)
                        # print json.dumps(current_dict, indent=4)

                        # get important parameter
                        # openid
                        current_openid = current_dict['open_id']
                        # gold type number
                        current_type = current_dict['source']
                        # gold change value
                        current_integral = int(current_dict['integral'])
                        # transaction timestamp
                        current_datetime = current_dict['dateTime']
                        # # print current_openid, current_type, current_integral, current_datetime, current_datetime / 1000
                        # todayDate = getStringDateTimeByTimestamp(current_datetime / 1000)

                        # print current_openid, current_integral, current_type

                        if current_type not in type_list:
                            type_list.append(current_type)

                        is_Exist_type = False
                        record_type = ''
                        record_sum = 0
                        array_type_element_index = 0
                        # find user record by openid
                        user_info_record = db.user_info_new1.find_one({'open_id': current_openid})
                        if user_info_record:
                            # when openid is exists, find the type item and add it to the count.
                            if user_info_record.has_key('gold'):
                                # get [gold.type.type] == current_type
                                for i in range(0, len(user_info_record['gold']['type'])):
                                    record_type = user_info_record['gold']['type'][i]['type']
                                    record_sum = int(user_info_record['gold']['type'][i]['sum'])
                                    if record_type == current_type:
                                        array_type_element_index = i
                                        # accumulate sum
                                        record_sum += current_integral
                                        is_Exist_type = True
                                        break

                                # not find current type, then append current type data into array of 'gold.type'
                                if is_Exist_type == False:
                                    # add a group of [type, sum] values to the array of [gold.type]
                                    db.user_info_new1.update({'open_id': current_openid},
                                                             {'$push': {
                                                                 'gold.type': {'type': current_type,
                                                                               'sum': current_integral}}})
                                    # print 'U:', {{'type': current_type, 'sum': current_integral}}
                                else:
                                    # update sum value in array elements
                                    db.user_info_new1.update({'open_id': current_openid},
                                                             {'$set': {
                                                                 'gold.type.' + str(
                                                                     array_type_element_index) + '.sum': record_sum}},
                                                             False, True)
                                    # print 'U:', 'accumulate'
                            else:
                                update_json = {
                                    'gold': {
                                        'type': [
                                            {
                                                'type': current_type,
                                                'sum': current_integral
                                            }
                                        ]
                                    }
                                }
                                db.user_info_new1.update({'open_id': current_openid}, {'$set': update_json})
                                # print 'U:', update_json
                        else:
                            insert_json = {
                                'open_id': current_openid,
                                'gold': {
                                    'type': [
                                        {
                                            'type': current_type,
                                            'sum': current_integral
                                        }
                                    ]
                                }
                            }
                            # db.user_info_new1.insert(insert_json)
                            # print 'I:', insert_json
                            # when openid does not exist, add a new user record with a typed item.
                        loop_index += 1
                        if loop_index % 1000 == 0:
                            print loop_index
                    print filename, loop_index
                    exit(1)



    except Exception as ex:
        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(ex)
        print '\ttraceback.format_exc():\n%s' % traceback.format_exc()
        exit(1)
    finally:
        type_list.sort()
        print 'type: ', type_list
        end_time = datetime.datetime.now()
        print str('total time: ' + str(end_time - start_time))
        print 'process is over.'
