#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import os
import time
# import zipfile
import traceback
import platform
import config


def getFileNameTuple(filename):
    # split the file_name and file_ext
    return os.path.splitext(filename)


def getSystemType():
    # return the type of system
    return platform.system()


if __name__ == '__main__':
    rootDirectory = './log/'
    tarDirectory = rootDirectory + 'tar/'
    compress_cmd_line = ''

    md5_set_file = None
    md5_dictionary = {}

    try:
        system_name = getSystemType()

        # create tar pack directory
        if os.path.exists(tarDirectory) == False:
            os.mkdir(tarDirectory)
        # change root directory
        os.chdir(rootDirectory)

        while (1):
            try:
                md5_set_file = open('./tar/' + config.MD5_FILE, 'w')
                md5_dictionary = {}
                for parent, dirnames, filenames in os.walk('.'):
                    for filename in filenames:  # 输出文件信息
                        nameTuple = getFileNameTuple(filename)
                        if nameTuple[1] == '.log':
                            # 压缩此文件
                            log_name_no_ext = nameTuple[0]
                            zip_pack_file_name = log_name_no_ext + '.tar.gz'

                            '''
                            # compress log file by zipfile libs.
                            z = zipfile.ZipFile(log_name_no_ext + '.zip', 'w')
                            z.write(filename, compress_type=zipfile.ZIP_DEFLATED)
                            z.close()

                            os.remove(os.path.join(parent, filename))
                            '''

                            compress_cmd_line = 'tar -czf ' + './tar/' + zip_pack_file_name + ' ' + filename
                            r = os.system(compress_cmd_line)
                            if r != 0:
                                continue
                            else:
                                # compress success, delete the log file
                                # os.system('rm -rf ' + filename)
                                # get the md5 value of the zip pack file
                                if system_name == 'Darwin':
                                    current_md5 = str(
                                        os.popen('md5 ' + './tar/' + zip_pack_file_name).read().split()[3])
                                elif system_name == 'Linux':
                                    current_md5 = str(
                                        os.popen('md5sum ' + './tar/' + zip_pack_file_name).read().split()[0])
                                else:
                                    continue

                                # md5_string = ''
                                # md5_string = {zip_pack_file_name: current_md5}
                                # md5_set_file.write(str(md5_string) + '\n')
                                # md5_set_file.flush()

                                md5_dictionary[zip_pack_file_name] = current_md5

                                # time.sleep(0.1)
                    exit(1)
            except Exception as ex:
                print '\tException Description:\t', str(Exception)
                print '\tError message:\t\t', str(ex)
                print '\ttraceback.format_exc():\n%s' % traceback.format_exc()

                # file_log.write('Exception: \n')
                # file_log.write('\tException Description:\t' + str(Exception) + '\n')
                # file_log.write('\tError message:\t\t' + str(e) + '\n')
                # file_log.write('\ttraceback.format_exc():\n%s' % traceback.format_exc() + '\n')
                # file_log.flush()

            # sleep 2 seconds in the end of every loop
            time.sleep(2)

    except Exception as e:

        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(e)
        print '\ttraceback.format_exc():\n%s' % traceback.format_exc()

        # file_log.write('Exception: \n')
        # file_log.write('\tException Description:\t' + str(Exception) + '\n')
        # file_log.write('\tError message:\t\t' + str(e) + '\n')
        # file_log.write('\ttraceback.format_exc():\n%s' % traceback.format_exc() + '\n')
        # file_log.flush()

        md5_set_file.flush()
        md5_set_file.close()
    finally:
        print 'md5 dictionary length: ', len(md5_dictionary)
        md5_set_file.write(str(md5_dictionary))
        md5_dictionary = {}
        md5_set_file.flush()
        md5_set_file.close()
        print 'md5 file write completed.'

        print 'process is over.'
        # file_log = open('process_log.log', 'a')
        # file_log.write('=======================================================\n')
        # file_log.write('=======================================================\n\n')
        # file_log.flush()
        # file_log.close()
