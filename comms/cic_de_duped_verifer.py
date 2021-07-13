"""
walk the cic-de-duped.sqlite DB and verify if files exist on disk

NOTE: once manual selection has started, we can EXPECT many files to be deleted.
So use of this module should be limited to folders and directores that have not yet
been manually processed

"""
import sys, os, shutil
from comms_db import CommsDBTable

DOWRITES = 0

class CommsDBRecord:

    def __init__ (self, data):
        self.data = data
        self.file_name = data[0]
        self.path = data[1]

def make_source_path_OLD (dst_path):
    return dst_path.replace ('/Volumes/cic-de-duped/', '/Volumes/archives/CommunicationsImageCollection/')

def make_source_path (dedup_path):
    base_dedup_path = '/Volumes/cic-de-duped/'
    base_archives_path = '/Volumes/archives/CommunicationsImageCollection/'
    rel_archives_path = dedup_path.replace (base_dedup_path, '')
    # Kludge for Stage / Field Projects
    if rel_archives_path.startswith('Field Projects'):
        rel_archives_path = rel_archives_path.replace('Field Projects', 'Staging')

    return os.path.join (base_archives_path, rel_archives_path)

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

            if DOWRITES:
                try:
                    shutil.copy2 (src, dst)
                    print '{} - wrote {}'.format(status, dst)
                except IOError, err:
                    print 'Copy error: {}'.format(err)
            else:
                # print '- would have copied {}: {}'.format(status, record.path)
                pass

            not_found.append(record.path)

        elif i > 0 and i % 100 == 0:
                print status

    return not_found


if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    db = CommsDBTable(sqlite_file)

    if 1:
        # where_clause = "where path LIKE '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc %'"
        # where_clause = "where path LIKE '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc 15/%'"
        where_clause = "where path LIKE '/Volumes/cic-de-duped/CIC-ExternalDisk6/%'"
        # where_clause = "WHERE path like '%cic-de-duped/Field Projects%'"
        records = db.select('file_name, path', where_clause)
        print '{} records selected'.format(len(records))
        not_found = verify_records(records)
        print '\n{} were not found'.format(len(not_found))
        for path in not_found:
            print path

    if 0:
        records = db.select_all_records()
        print '{} records in DB'.format(len(records))

        print records[1]

        start = 0
        batch = 100
        not_found = verify_records(records[start:(start + batch)])
        print '{} were not found'.format(len(not_found))
        for rec in not_found:
            print rec