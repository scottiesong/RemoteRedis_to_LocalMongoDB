#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import os
import traceback

if __name__ == '__main__':
    total_count = 0
    try:
        for parent, dirnames, filenames in os.walk('.'):
            for filename in filenames:  # 输出文件信息
                if os.path.splitext(filename)[1] == '.log':
                    lines = int(os.popen('wc -l ' + filename).read().split()[0])
                    total_count += lines
                    print filename, lines


    except Exception as ex:
        print '\tException Description:\t', str(Exception)
        print '\tError message:\t\t', str(ex)
        print '\ttraceback.format_exc():\n%s' % traceback.format_exc()

    finally:
        print 'total lines: ', total_count
