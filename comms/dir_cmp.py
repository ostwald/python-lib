"""
Are all the photos under dirA contained in dirB?
here we are using checksum as key
"""

import os, sys, sqlite3
from comms_db import CommsDBTable

class DirCmp:

    def __init__ (self, sqlite_file):
        self.db = CommsDBTable(sqlite_file)

    def compare (self, dirA, dirB):
        dirA_items = self.get_dir_items(dirA)
        dirA_cksums = map (lambda x:x[0], dirA_items)

        dirB_items = self.get_dir_items(dirB)
        dirB_cksums = map (lambda x:x[0], dirB_items)

        print '{} chksums in DirA'.format(len(dirA_cksums))
        print '{} chksums in DirB'.format(len(dirB_cksums))

        print 'Items in {} but not in {}'.format(dirA, dirB)
        for n in dirA_cksums:
            if not n in dirB_cksums:
                print n

    def get_dir_items(self, path):
        rows = self.db.select ('check_sum, path', "WHERE path LIKE '{}%'".format(path))
        return rows

if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/tmp/TEST_composite/TEST_composite.sqlite'
    base_dir = '/Volumes/archives/CommunicationsImageCollection'
    dirA = os.path.join(base_dir, 'CarlyeMainDisk2/NCAR digital photos/1-archived')
    dirB = os.path.join(base_dir, 'CIC-ExternalDisk1/photos/1-archived')


    dc = DirCmp(sqlite_file)
    dc.compare(dirA, dirB)
