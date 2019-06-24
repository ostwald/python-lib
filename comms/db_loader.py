import os, sys, re
import globals
from jloFS import JloFile
from comms_db import CommsDBTable
from walker import Walker

class LoadingWalker (Walker):

    def __init__ (self, start_dir):
        Walker.__init__(self, start_dir)

        self.db_table = CommsDBTable()

    def process_image (self, path):
        img_file = JloFile(path)
        self.db_table.add_record(img_file)

def load_db_from_path (path):
    walker = LoadingWalker(root)
    walker.walk()
    print '\n{}'.format(root)
    print 'files: {}   imnage files: {}   dirs: {}  elapsed: {}'.format(walker.file_cnt, walker.image_cnt, walker.dir_cnt, walker.elapsed)
    print 'unknown_extensions:', walker.unknown_extensions
    print 'skipped directories'
    for d in walker.skipped_directories:
        print '-', d

if __name__ == '__main__':
    # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/'
    root = '/Users/ostwald/tmp/test_comms_file_structure/'
    # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 5'
    load_db_from_path(root)