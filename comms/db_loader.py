import os, sys, re
import globals
from jloFS import JloFile
from comms_db import CommsDBTable
from walker import Walker

class AlreadyExistsError (Exception):
    pass

class LoadingWalker (Walker):

    def __init__ (self, start_dir, sqlitefile):

        if os.path.exists (sqlitefile):
            raise AlreadyExistsError, '\nERROR: sqlite_file already exists at {}\n'.format(sqlitefile)

        Walker.__init__(self, start_dir)

        self.db_table = CommsDBTable(sqlitefile)

    def process_image (self, path):
        img_file = JloFile(path)
        self.db_table.add_record(img_file)

def load_db_from_path (root, sqlitefile):
    walker = LoadingWalker(root, sqlitefile)
    walker.walk()
    print '\n{}'.format(root)
    print 'files: {}   image files: {}   dirs: {}  elapsed: {}'.format(walker.file_cnt, walker.image_cnt, walker.dir_cnt, walker.elapsed)
    print 'unknown_extensions:', walker.unknown_extensions
    if 0:
        print 'skipped directories'
        for d in walker.skipped_directories:
            print '-', d

class AutoLoader:

    file_root = '/Volumes/archives/CommunicationsImageCollection/'
    db_root = '/Users/ostwald/Documents/Comms/'

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
                    # load_db_from_path(path, sqlite_file)
                    print 'path: {}, sqlite_file: {}'.format(path, sqlite_file)
                except AlreadyExistsError:
                    print sys.exc_info()[1]


    def accept_top_level_dir (self, path):
        if not os.path.isdir (path):
            return False
        name = os.path.basename(path)
        if name.endswith('Try'):
            return False
        # return name.startswith ('Carlye') or name.startswith ('CIC')
        return True

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


    if 0:  # load a list of dirs
        dir_names = ['Field Projects', 'VideoEditingDisk1','VideoEditingDisk2']
        comms_dir = '/Users/ostwald/Documents/Comms'
        data_dir = '/Volumes/archives/CommunicationsImageCollection'

        for dir_name in dir_names:
            root = os.path.join (data_dir, dir_name)
            sqlite_file = os.path.join (comms_dir, dir_name, dir_name + '.sqlite')

            print '\n',root
            print ' - ',sqlite_file

            try:
                load_db_from_path(root, sqlite_file)
            except AlreadyExistsError:
                print sys.exc_info()[1]

    if 1: #
        sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped-VERIFY.sqlite'
        root = '/Volumes/cic-de-duped'
        load_db_from_path(root, sqlite_file)
