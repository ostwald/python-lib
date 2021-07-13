import os, sys, re
import globals
import sqlite3

from comms_db import CommsDBTable

def get_num (filename):
    """

    :param filename:
    :return:
    """

    if filename[0] == '.':
        return None
    root = os.path.splitext(filename)[0]
    pat = re.compile("([0-9]+)")
    m = pat.findall (root)
    m.sort (key=lambda x: -int(x))

    # print m

    if m and len(m[0]) > 3:
        return m[0]
    else:
        return None

class ImageRange:

    def __init__ (self, start):
        self.start = start
        self.end = None

    def __repr__ (self):
        if self.end is None:
            return self.start
        else:
            return '{}-{}'.format(self.start,self.end)

class DirLister:

    """
    Does listing and reporting over File Directories
    """

    def __init__ (self, base_dir, level=0, recursive=True):
        self.base_dir = base_dir
        if base_dir.endswith('87'):
            base_dir += ' '
        self.level = level
        self.recursive = recursive
        self.INDENT = level*'   '


    def get_file_names (self):
        """
        return a list of file names (not dir names
        :return:
        """
        names = os.listdir(self.base_dir)
        return filter (lambda x:os.path.isfile(os.path.join (self.base_dir, x)), names)

    def get_subdirs (self):
        """
        return sub directory paths for base_dir
        :return:
        """
        subdirs = []
        for filename in os.listdir(self.base_dir):
            if filename[0] == '.':
                continue

            path = os.path.join (self.base_dir, filename)
            if os.path.isdir(path):
                subdirs.append(path)
        return subdirs


    def list_img_spans (self, file_names=None):

        ranges = []
        last = None

        if file_names is None:
            file_names = self.get_file_names()
        # file_nums = filter (None, map (get_num, os.listdir (path)))
        file_nums = filter (None, map (get_num, file_names))
        file_nums.sort()

        # print file_nums

        for num in file_nums:
            # if len (ranges) == 0:
            #     new_range = ImageRange(num)
            #     ranges.append (new_range)
            if num == last: continue

            if last is None or int(num) != int(last) + 1:
                if len(ranges) > 0 and last is not None and last != ranges[-1].start:
                    ranges[-1].end = last
                new_range = ImageRange(num)
                ranges.append (new_range)

            last = num

        if len(ranges) > 0 and last != ranges[-1].start:
            ranges[-1].end = last

        return ', '.join (map (lambda x: str(x), ranges))


    def report_file_names (self):

        if self.level == 0:
            print self.base_dir

        print '\n{}{}'.format(self.INDENT, os.path.split(self.base_dir)[1])
        img_spans = self.list_img_spans ()
        file_names = self.get_file_names()
        for name in file_names:
            print '{} - {}'.format(self.INDENT,name)

        if self.recursive:
            for p in self.get_subdirs():
                self.__class__(p, level=self.level+1, recursive=self.recursive).report_file_names()

    def report (self):
        if self.level == 0:
            print self.base_dir

        print '\n{}{}'.format(self.INDENT, os.path.split(self.base_dir)[1])
        img_spans = self.list_img_spans ()
        if len(img_spans.strip()) > 0:
            print '{}{}'.format(self.INDENT,img_spans)

        if self.recursive:
            for p in self.get_subdirs():
                self.__class__(p, level=self.level+1, recursive=self.recursive).report()

class  DBDirLister (DirLister):
    """
    Provides Listing tools operating over a DB (rather than a file system)
    """

    def __init__ (self, base_dir, level=0, recursive=True):
        DirLister.__init__ (self, base_dir, level, recursive)
        self.db = CommsDBTable(globals.composite_sqlite_file)
        self.all_names = self.db.list_dir(self.base_dir)

    def get_file_names (self):
        return filter (lambda x:globals.isImage(x), self.all_names)

    def get_subdirs (self):
        dirnames = filter (lambda x:not globals.isImage(x), self.all_names)
        return map (lambda x: os.path.join (self.base_dir, x), dirnames)

    def report_file_names (self):
        """
        use DupManager to mark duplicates
        :return:
        """
        if self.level == 0:
            print self.base_dir

        img_spans = self.list_img_spans ()
        file_names = self.get_file_names()

        print '\n{}{}   ({})'.format(self.INDENT, os.path.split(self.base_dir)[1], len(file_names))

        for name in file_names:
            dup_star = is_dup(os.path.join (self.base_dir, name)) and '* ' or ''
            print '{} - {}{}'.format(self.INDENT,dup_star,name)

        if self.recursive:
            for p in self.get_subdirs():
                self.__class__(p, level=self.level+1, recursive=self.recursive).report_file_names()


if __name__ == '__main__':

    if 0: # DEFAULT - called by __init__.py
        if len(sys.argv) > 1:
            disc_num = sys.argv[1]
            path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc {}'.format(disc_num)
            DirLister(path).report()
        else:
            print 'disc_num required'

    if 1:
        # path = '/Volumes/archives/CommunicationsImageCollection/CarlyeMainDisk2/NCAR digital photos/1-archived/ASP/'
        path = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc 143/NWSC-6-4-12 (Part 3)'
        DirLister(path).report()
    if 0:
        # path = '/Volumes/archives/CommunicationsImageCollection/CarlyeMainDisk2/NCAR digital photos/1-archived/ASP/'
        path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk6'
        lister = DBDirLister(path)

        for p in lister.all_names:
            print p

        lister.report_file_names()

        where_clause = "WHERE path LIKE '{}%'".format(path)
        print "TOTAL FILES: {}".format(lister.db.count_selected(where_clause))

    if 0:
        num_str = "08x }'97dgy238742.JPG"
        num = get_num("08972.JPG")
        print '- num_str: "{}" get_num: "{}" ({})'.format(num_str, num, type (num))