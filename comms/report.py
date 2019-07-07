import sys, os, re, time, json

import sqlite3

db_file = '/Users/ostwald/tmp/comms_db.sqlite'
table_name = 'comms_files'

class TableReporter:
    sqlite_file = '/Users/ostwald/tmp/test_db.sqlite'
    table_name = 'comms_files'

    def __init__ (self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

def get_distinct_values(field_name):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # get total
    query = "SELECT DISTINCT ({fn}) FROM `{tn}` ".format(fn=field_name, tn=table_name)

    # print total_query

    c.execute(query)
    rows = c.fetchall()

    return map (lambda x:x[0], rows)

def get_unique_extensions():
    return get_distinct_values('extension')

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

def extension_reporter ():
    extensions = get_unique_extensions()
    extensions.sort()

    print 'Extension Diskspace'
    for ext in extensions:
        count = get_count_for_extension(ext)
        bytes = get_diskspace_for_extension(ext)

        # print '- {} : {} bytes'.format(ext,bytes)
        print '- {} - {} files - {} MB total'.format(ext, count, int(bytes/1000000))

def get_paths (field_name, field_value):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # get total
    query = "SELECT path FROM `{tn}` WHERE {fn} = '{fv}'" \
        .format(tn=table_name, fn=field_name, fv=field_value)

    # print total_query

    c.execute(query)
    rows = c.fetchall()

    return map (lambda x:x[0], rows)

# How to find all dups??
def find_dups(field_name):
    """
    last_dup_value = None
    collected_paths = []
    for row in rows:
        dup_value = XX
        if dup_value != last_dup_value:
            if len(collected_paths > 1):
                dups[last_dup_value] = collected_paths
            collected_paths = path
            last_dup_value = dup_value
        collected_paths.append(path)

    :param field_name:
    :return:
    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # get total
    query = "SELECT path, {fn} FROM `{tn}` ORDER BY {on}" \
        .format(tn=table_name, fn=field_name, on=field_name)

    c.execute(query)
    rows = c.fetchall()

    dup_map = {}
    last_value = None
    collected_paths = []
    for row in rows:
        dup_value = row[1]
        path = row[0]
        if dup_value != last_value:
            if len(collected_paths) > 1:
                dup_map[last_value] = collected_paths
            collected_paths = [path,]
            last_value = dup_value
        else:
            collected_paths.append(path)
    if len(collected_paths) > 1:
        dup_map[last_value] = collected_paths
    return dup_map


def write_dups (field):
    dups = find_dups(field)
    dups_dir = '/Users/ostwald/Documents/Comms/comms_CIC-ExternalDisk1/dups'
    outpath = os.path.join (dups_dir, field + '_dups.json')
    fp = open(outpath, 'w')
    fp.write( json.dumps(dups, sort_keys=True, indent=4, separators=(',', ': ')))
    fp.close()
    print 'wrote dups to {}'.format(outpath)

if __name__ == '__main__':
    # rows = get_paths('file_name', '_MG_0194.jpg')
    # print rows

    field = 'check_sum'
    write_dups (field)
