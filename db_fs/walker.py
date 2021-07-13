"""
Walks the files and subdirectories of a given path, calling process_file
on each it encounters
"""
import os, sys, time, re
from comms import CommsDBTable
from jloFS import JloFile

class FSWalker:
    """
    Abstract (but FileSystem-oriented) Walker. Concrete instances overwrite process_file, etc
    """
    accept_file_rules = []
    accept_dir_rules = []


    # known_extentions = globals.KNOWN_EXTENSIONS
    # target_extensions = globals.IMAGE_EXTENSIONS  # extns to process
    # skip_dir_names = globals.SKIP_DIR_NAMES
    # skip_dir_name_frags = globals.SKIP_DIR_NAME_FRAGS

    def __init__ (self, start_dir):
        self.start_dir = start_dir
        self.all_file_cnt = 0
        self.file_cnt = 0
        self.dir_cnt = 0
        self.elapsed = 0
        self.unknown_extensions = []
        self.known_extensions = []
        self.skipped_directories = []

    def accept_file (self, path):
        # print 'accept file'
        for rule in self.accept_file_rules:
            # print 'rule: {}'.format(type(rule))
            # ALL rules must be true
            if type(rule) == type(lambda x:x):
                if not rule(path):
                    return False
            if type(rule) in [type (''), type(u'')]:
                # print ' about to do a search boss ({}, {})'.format(rule, path)
                m = re.compile(rule).search (path)
                if m is None:
                    # print '{} was not found in {}'.format(rule, path)
                    return False
                else:
                    # print '{} was found in {}'.format(rule, path)
                    pass

        return True

    def accept_dir(self, path):
        dirname = os.path.basename(path)

        for rule in self.accept_dir_rules:
            # blacklist things (hits) must return false
            if type(rule) == type(lambda x:x):
                if not rule(path):
                    return False
            if type(rule) in [type (''), type(u'')]:
                m = re.compile(rule).search (path)
                if m is None:
                    # print '{} was not found in {}'.format(rule, path)
                    return False
                else:
                    # print '{} was found in {}'.format(rule, path)
                    pass
        return True

    def process_file (self, path):
        pass

    def walk (self):
        tics = time.time()
        for root, dirs, files in os.walk(self.start_dir, topdown=True):
            print root

            to_remove = []
            for d in dirs:
                path = os.path.join (root, d)
                if not self.accept_dir(path):
                    to_remove.append(d)
                    self.skipped_directories.append(path)
            for d in to_remove:
                dirs.remove(d)
                # print 'removed {}'.format(d)

            for name in files:
                path = os.path.join (root, name)
                ext = os.path.splitext(name)[1]

                if not ext in self.known_extensions and not ext in self.unknown_extensions:
                    self.unknown_extensions.append(ext)

                self.all_file_cnt += 1

                # this can be expressed as white/black list
                # if ext.lower() in self.target_extensions:
                if self.accept_file(path):
                    self.file_cnt += 1
                    self.process_file(path)
                else:
                    print 'rejected file: {}'.format(path)

            for name in dirs:
                # print(os.path.join(root, name))
                self.dir_cnt += 1

        self.elapsed = time.time() - tics

class AlreadyExistsError (Exception):
    pass


class LoadingWalker (FSWalker):
    """
    Concrete Walker that writes to a database
    """
    def __init__ (self, start_dir, sqlitefile):

        FSWalker.__init__(self, start_dir)
        self.db_table = CommsDBTable(sqlitefile)

    def process_file (self, path):
        img_file = JloFile(path)
        self.db_table.add_record(img_file)

class SafeLoadingWalker (LoadingWalker):

    def __init__ (self, start_dir, sqlitefile, safe=True):
        self.safe = safe

        # if self.safe and os.path.exists (sqlitefile):
        #     raise AlreadyExistsError, '\nERROR: sqlite_file already exists at {}\n'.format(sqlitefile)

        LoadingWalker.__init__(self, start_dir, sqlitefile)

    def process_file (self, path):
        """
        only process if there is NOT already an entry in the database for this path
        :param path:
        :return: processes only if path is not in DB
        """
        img_file = JloFile(path)
        where_clause = "WHERE path='{}'".format(path.replace("'", "''"))
        found = self.db_table.count_selected (where_clause)
        try:
            found = int (found)
        except:
            print sys.exc_info()[1]
            found = 0
        # print 'rec found: {}'.format(found)
        if found > 0 and self.safe:
            # print 'skipping ...'
            pass
        else:
            # print 'writing ...'
            self.db_table.add_record(img_file)
            pass


if __name__ == '__main__':
    # root = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos/'
    # walker = Walker(root)
    # walker.walk()
    # print '\n{}'.format(root)
    # print 'files: {}   imnage files: {}   dirs: {}  elapsed: {}'.format(walker.all_file_cnt, walker.file_cnt, walker.dir_cnt, walker.elapsed)
    # print 'unknown_extensions:', walker.unknown_extensions
    # print 'skipped directories'
    # for d in walker.skipped_directories:
    #     print '-', d

    pass