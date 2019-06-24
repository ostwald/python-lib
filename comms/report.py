import sys, os, re, time

import sqlite3

db_file = '/Users/ostwald/tmp/test_db.sqlite'
table_name = 'comms_files'

class TableReporter:
    sqlite_file = '/Users/ostwald/tmp/test_db.sqlite'
    table_name = 'comms_files'

    def __init__ (self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()


def get_unique_extensions():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # get total
    total_query = "SELECT DISTINCT (extension) FROM `{tn}` ".format(tn=table_name)

    # print total_query

    c.execute(total_query)
    rows = c.fetchall()

    return map (lambda x:x[0], rows)

def get_count_for_extension (ext):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # get total
    query = "SELECT COUNT (extension) FROM `{tn}` WHERE extension = '{tv}'" \
        .format(tn=table_name, tv=ext)

    c.execute(query)
    return  c.fetchone()[0]

def get_diskspace_for_extension (ext):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # get total
    query = "SELECT SUM (size) FROM `{tn}` WHERE extension = '{tv}'" \
        .format(tn=table_name, tv=ext)

    c.execute(query)
    return  c.fetchone()[0]

def report_extension_counts ():
    extensions = get_unique_extensions()
    extensions.sort()

    print 'Extension Counts'
    for ext in extensions:
        c = get_count_for_extension(ext)
        print '- {} : {}'.format(ext,c)

def report_extension_diskspace():
    extensions = get_unique_extensions()
    extensions.sort()

    print 'Extension Diskspace'
    for ext in extensions:
        bytes = get_diskspace_for_extension(ext)
        # print '- {} : {} bytes'.format(ext,bytes)
        print '- {} : {} MB'.format(ext,int(bytes/1000000))


if __name__ == '__main__':
    report_extension_counts()
    report_extension_diskspace()
    if 0:
        extensions = get_unique_extensions()
        print extensions

        for ext in extensions:
            print '-', ext
    if 0:
        ext = '.tif'
        c = get_count_for_extension(ext)
        print 'COUNT: ', c