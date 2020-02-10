"""
walk the cic-de-duped.sqlite DB and verify if files exist on disk


"""
import sys, os, shutil
from comms_db import CommsDBTable

class CommsDBRecord:

    def __init__ (self, data):
        self.data = data
        self.file_name = data[0]
        self.path = data[1]

def make_source_path (dst_path):
    return dst_path.replace ('/Volumes/cic-de-duped/', '/Volumes/archives/CommunicationsImageCollection/')

def verify_records (records):
    not_found = []
    for i, record in enumerate(map (CommsDBRecord, records)):

        status = '{}/{}'.format(i, len(records))
        if not os.path.exists(record.path):
            # print '{}: {}'.format(status, record.path)

            # make the source path and then copy

            dst = record.path
            src = make_source_path (record.path)
            # print 'dst: {}'.format(record.path)
            # print 'src: {}'.format(src)

            try:
                shutil.copyfile (src, dst)
                print '{} - wrote {}'.format(status, dst)
                not_found.append(record.path)

            except IOError, err:
                print 'Copy error: {}'.format(err)



        elif i > 0 and i % 1000 == 0:
                print status

    return not_found


if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    db = CommsDBTable(sqlite_file)

    records = db.select_all_records()
    print '{} records in DB'.format(len(records))

    print records[1]

    start = 0
    batch = 100000
    not_found = verify_records(records[start:(start + batch)])
    print '{} were not found'.format(len(not_found))