import os, sys, re
import globals
from jloFS import JloFile
from comms import CommsDBTable
from walker import SafeLoadingWalker, AlreadyExistsError

class AutoLoader:

    def __init__(self, file_root, db_root):
        self.file_root = file_root
        self.db_root = db_root

    def process (self):
        for filename in os.listdir(self.file_root):
            path = os.path.join (self.file_root, filename)
            if self.accept_top_level_dir(path):
                print filename
                db_dir = os.path.join (self.db_root, filename)
                if not os.path.exists(db_dir):
                    os.mkdir (db_dir)
                sqlite_file = os.path.join (db_dir, filename+'.sqlite')
                try:
                    load_db_from_path(path, sqlite_file)
                except AlreadyExistsError:
                    print sys.exc_info()[1]

    def accept_top_level_dir (self, path):
        if not os.path.isdir (path):
            return False
        name = os.path.basename(path)
        if name.endswith('Try'):
            return False
        return name.startswith ('Carlye') or name.startswith ('CIC')

def load_db_from_path (root, sqlitefile):
    walker = SafeLoadingWalker(root, sqlitefile)
    walker.walk()
    print '\n{}'.format(root)
    print 'files: {}   imnage files: {}   dirs: {}  elapsed: {}'.format(walker.all_file_cnt, walker.file_cnt, walker.dir_cnt, walker.elapsed)
    print 'unknown_extensions:', walker.unknown_extensions
    if 0:
        print 'skipped directories'
        for d in walker.skipped_directories:
            print '-', d


if __name__ == '__main__':

    if 0:
        # sqlite_file = '/Users/ostwald/tmp/CarlyeMainDisk2.sqlite'
        sqlite_file = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk1/CIC-ExternalDisk1.sqlite'

        root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/'
        # root = '/Volumes/archives/CommunicationsImageCollection/CarlyeMainDisk2'
        # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternallDisk1SecondTry/'
        # root = '/Users/ostwald/tmp/test_comms_file_structure/'
        # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 5'
        # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 9/courtney - daycare/'
        load_db_from_path(root, sqlite_file)

    if 0:
        loader = AutoLoader()
        loader.process()
        # print loader.accept_top_level_dir('/Volumes/archives/CommunicationsImageCollection/CIC-ExternallDisk1SecondTry/')