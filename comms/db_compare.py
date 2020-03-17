import sys, os, re
import sqlite3

from comms_db import CommsDBTable

"""
compares DBs with directories on disk
"""

class CompDB (CommsDBTable):

    def __init__ (self, sqlite_file, base_dir):
        self.base_dir = base_dir
        self.sqlite_file = sqlite_file
        conn = sqlite3.connect(self.sqlite_file)
        self.cursor = conn.cursor()

    def get_dirs(self, rel_dir=''):
        """
        get a list of top-level directories using file system
        - nonb-recursive

        - rel_dir is path relative to self.base_dir

        """

        root_dir =  os.path.join (self.base_dir, rel_dir)
        dirs = []
        for filename in os.listdir(root_dir):
            if filename[0] == '.':
                continue
            path = os.path.join (root_dir, filename)
            if os.path.isdir(path):
                dirs.append (path)
        return dirs

    def get_dir_names(self, rel_dir=''):
        return map(lambda x:os.path.basename(x), self.get_dirs())

    def get_dir_count (self, rel_dir=''):
        dirname = os.path.join (self.base_dir, rel_dir)
        query = "SELECT COUNT(*) FROM comms_files WHERE path LIKE '{}%'".format(dirname)
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        # return map(lambda x:x[0], rows)
        return int(row[0])

    def get_dir_size (self, rel_dir=''):
        """
        Return total disk space taken by images in specified directory (in MB)
        :param dirname:
        :return:
        """
        dirname = os.path.join (self.base_dir, rel_dir)
        query = "SELECT SUM(size) FROM comms_files WHERE path LIKE '{}%'".format(dirname)
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        # return map(lambda x:x[0], rows)

        raw = row[0]
        if raw is None:
            return 0
        else:
            return int (int(raw)/10000000)

    def get_dir_paths (self, rel_dir=''):
        dirname = os.path.join (self.base_dir, rel_dir)
        query = "SELECT path FROM comms_files WHERE path LIKE '{}%'".format(dirname)
        print query
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return map(lambda x:x[0], rows) # return only paths

    def get_relative_path (self, path, rel_dir=''):
        root = os.path.join (self.base_dir, rel_dir)
        return path.replace (root, '')


class DBCompare:
    """
    We want to look at the top level directories and make some simple comparisons,
    like number of image files, and size (within that directory)
    """
    def __init__ (self, db_cmpA, db_cmpB):
        self.db_cmpA = db_cmpA
        self.db_cmpB = db_cmpB

    def get_directory_list (self):
        return list(set (self.db_cmpA.get_dir_names() + self.db_cmpB.get_dir_names()))

    def dir_comp_stats (self, d):

        if not d.endswith('/'):
            d += '/'

        sizeA = self.db_cmpA.get_dir_size(d)
        countA = self.db_cmpA.get_dir_count(d)

        sizeB = self.db_cmpB.get_dir_size(d)
        countB = self.db_cmpB.get_dir_count(d)

        return sizeA, countA, sizeB, countB

    def compare_top_dirs (self):
        for d in self.get_directory_list():
            # sizeA = self.db_cmpA.get_dir_size(d)
            # countA = self.db_cmpA.get_dir_count(d)
            #
            # sizeB = self.db_cmpB.get_dir_size(d)
            # countB = self.db_cmpB.get_dir_count(d)

            sizeA, countA, sizeB, countB = self.dir_comp_stats (d)

            if sizeA != sizeB or countA != countB:
                print '{}\t{}\t{}\t{}\t{}'.format(d,sizeA, sizeB, countA, countB)

        print '\n .. compare_top_dirs is complete'

    def compare_dir (self, rel_dir):

        if not rel_dir.endswith('/'):
            rel_dir += '/'

        sizeA, countA, sizeB, countB = self.dir_comp_stats (rel_dir)
        print 'sizeA: {}, countA: {}'.format(sizeA, countA)
        print 'sizeB: {}, countB: {}'.format(sizeA, countA)

        raw_pathsA = self.db_cmpA.get_dir_paths(rel_dir)
        raw_pathsB = self.db_cmpB.get_dir_paths(rel_dir)

        pathsA = map (lambda x:self.db_cmpA.get_relative_path(x, rel_dir), raw_pathsA)
        pathsB = map (lambda x:self.db_cmpB.get_relative_path(x, rel_dir), raw_pathsB)

        print '{} in pathsA'.format(len(pathsA))
        print '{} in pathsB'.format(len(pathsB))

        # pathsA.sort()
        # for p in pathsA:
        #     print p


        print 'paths in A but not in B'
        for path in pathsA:
            if path not in pathsB:
                print '-', path
            # else:
            #     print pathsB.index(path)

        print 'paths in B but not in A'
        for path in pathsB:
            if path not in pathsA:
                print '-', path

if __name__ == '__main__':
    sqlite_fileA = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk1/CIC-ExternalDisk1.sqlite'
    pathA = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/'
    cmpA = CompDB (sqlite_fileA, pathA)


    if 0:
        dir_name = 'design and work files'
        countA = cmpA.get_dir_count(os.path.join (pathA, dir_name))
        print '{} files for {}'.format( countA, dir_name)
        sizeA = cmpA.get_dir_size(os.path.join (pathA, dir_name))
        print '{} MB for {}'.format( sizeA, dir_name)


    if 1:
        sqlite_fileB = '/Users/ostwald/Documents/Comms/CIC-ExternallDisk1SecondTry/ExternallDisk1SecondTry.sqlite'
        pathB = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternallDisk1SecondTry/'
        cmpB = CompDB (sqlite_fileB, pathB)

        db_cmp = DBCompare (cmpA, cmpB)
        # for d in sorted(db_cmp.get_directory_list()):
        #     print d
        db_cmp.compare_top_dirs()

        # db_cmp.compare_dir('disc 7/')