"""
Are all the photos under dirA contained in dirB?
here we are using checksum as key
"""

import os, sys, sqlite3
from comms_db import CommsDBTable
import globals

class DirCmp:

    verbose = 0

    def __init__ (self, sqlite_file):
        self.db = CommsDBTable(sqlite_file)

    def compare (self, dirA, dirB):
        dirA_items = self.get_dir_items(dirA)
        dirA_cksums = map (lambda x:x[0], dirA_items)

        dirB_items = self.get_dir_items(dirB)
        dirB_cksums = map (lambda x:x[0], dirB_items)

        print 'DirA: {} ({} chksums)'.format(dirA, len(dirA_cksums))
        print 'DirB: {} ({} chksums)'.format(dirB, len(dirB_cksums))

        # print 'Items in {} but not in {}'.format(dirA, dirB)
        items = []
        for n in dirA_cksums:
            if not n in dirB_cksums:
                items.append(n)
        print '{} Items in dirA but not in dirB'.format(len(items))

        if self.verbose:
            for n in items:
                print n

    def get_dir_items(self, path):
        rows = self.db.select ('check_sum, path', "WHERE path LIKE '{}%'".format(path))
        return rows

    def get_sub_dirs_OFF (self, path):
        base_dir = os.path.dirname(path)
        segments = len(base_dir.split('/'))
        items = self.get_dir_items (base_dir)
        sub_dirs = []
        for item in items:
            sub_dir = os.path.dirname(item[1])
            if len(sub_dir.split('/')) == segments + 1:
                sub_dirs.append(sub_dir)
        return list (set( sub_dirs))

    def get_sub_dirs (self, path):
        base_dir = os.path.dirname(path)
        base_dir_len = len(base_dir.split('/'))
        items = self.get_dir_items (base_dir)
        print '{} items in {}'.format(len(items), path)
        sub_dirs = []
        child_names = []
        for item in items:
            dir_path = os.path.dirname(item[1])
            splits = dir_path.split('/')
            if len(splits) > base_dir_len:
                child_name = splits[base_dir_len]
                if not child_name in child_names:
                    child_names.append (child_name)
        return map (lambda x:os.path.join (path, x), child_names)

    def top_level_compare (self, dirA, dirB):
        subDirsA = self.get_sub_dirs(dirA)
        subDirsB = self.get_sub_dirs(dirB)

        print '\nsubDirsA'
        for s in subDirsA:
            print s


        print '\nsubDirsB'
        for s in subDirsB:
            print s

        for subDirA in subDirsA:
            name = os.path.basename(subDirA)
            # print name
            subDirB = os.path.join (dirB, name)
            # if subDirsB.index (subDirB) > -1:
            if subDirB in subDirsB:
                print '\n{} is in both'.format(name)
                dc.compare(subDirA, subDirB)
                dc.compare(subDirB, subDirA)
            else:
                print '\n{} is in A but not in B'.format(name)


def compare_directories (dirA, dirB):
    sqlite_file = globals.composite_sqlite_file
    dc = DirCmp(sqlite_file)
    dc.compare(dirA, dirB)
    dc.compare(dirB, dirA)

if __name__ == '__main__':
    base_dir = '/Volumes/archives/CommunicationsImageCollection'

    if 0:   # compare directories
        dirA = os.path.join(base_dir, 'CarlyeMainDisk2/NCAR digital photos/need to be archived/')
        dirB = os.path.join(base_dir, 'CIC-ExternalDisk1/photos/need to be archived/')
        compare_directories (dirA, dirB)

    if 0:
        sqlite_file = globals.composite_sqlite_file
        dc = DirCmp(sqlite_file)
        rel_path = 'CarlyeMainDisk2/NCAR digital photos/need to be archived/'
        rel_path = 'CIC-ExternalDisk1/photos/need to be archived/'
        base_dir = os.path.join(base_dir, rel_path)
        subs = dc.get_sub_dirs(base_dir)
        for s in subs:
            print os.path.basename(s)

    if 1:   # compare directories
        dirA = os.path.join(base_dir, 'CarlyeMainDisk2/NCAR digital photos/need to be archived/')
        dirB = os.path.join(base_dir, 'CIC-ExternalDisk1/photos/need to be archived/')
        sqlite_file = globals.composite_sqlite_file
        # sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/Before Dedup-1/composite-BEFORE-DEDUP.sqlite'
        dc = DirCmp(sqlite_file)
        dc.top_level_compare(dirA, dirB)