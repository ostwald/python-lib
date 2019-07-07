import os, sys, re
import globals
from jloFS import JloFile
from comms_db import CommsDBTable
from walker import Walker

class LoadingWalker (Walker):

    def __init__ (self, start_dir, sqlitefile):
        Walker.__init__(self, start_dir)

        self.db_table = CommsDBTable(sqlitefile)

    def process_image (self, path):
        img_file = JloFile(path)
        self.db_table.add_record(img_file)

def load_db_from_path (path, sqlitefile):
    walker = LoadingWalker(root, sqlitefile)
    walker.walk()
    print '\n{}'.format(root)
    print 'files: {}   imnage files: {}   dirs: {}  elapsed: {}'.format(walker.file_cnt, walker.image_cnt, walker.dir_cnt, walker.elapsed)
    print 'unknown_extensions:', walker.unknown_extensions
    print 'skipped directories'
    for d in walker.skipped_directories:
        print '-', d

if __name__ == '__main__':

    sqlite_file = '/Users/ostwald/tmp/CarlyeMainDisk2.sqlite'

    # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/'
    root = '/Volumes/archives/CommunicationsImageCollection/CarlyeMainDisk2'
    # root = '/Users/ostwald/tmp/test_comms_file_structure/'
    # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 5'
    # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 9/courtney - daycare/'
    load_db_from_path(root, sqlite_file)