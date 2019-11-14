import os, sys, re
import globals
import sqlite3

from dir_lister import DirLister
from dup_manager import DupManager


class DupDirLister (DirLister):

    def __init__ (self, basedir, dups_path):
        dup_path = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'
        self.dup_mgr = DupManager(dup_path)

        basepath = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 145/HUB/HUB-event10-9-12/'
        DirLister.__init__(self, basepath)

    def report (self):
        if self.level == 0:
            print self.base_dir

        print '\n{}{}'.format(self.INDENT, os.path.split(self.base_dir)[1])
        # img_spans = self.list_img_spans ()
        # if len(img_spans.strip()) > 0:
        #     print '{}{}'.format(self.INDENT,img_spans)

        dups = self.list_dups ()
        file_names = sorted(dups.keys())

        for name in file_names:
            print '{} - {}'.format(self.INDENT,name)
            for d in dups[name]:
                print '{}   - {}'.format(self.INDENT,d)

        if self.recursive:
            for p in self.get_subdirs():
                self.__class__(p, level=self.level+1, recursive=self.recursive).report()


    def list_dups (self):
        dup_map = {}
        for file_name in self.get_file_names():
            path = os.path.join (self.base_dir, file_name)
            dups = self.dup_mgr.find_dups_for_file(path)
            if len(dups) > 0:
                dup_map[file_name] = dups
        return dup_map


if __name__ == '__main__':

    dup_path = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'
    # dup_mgr = DupManager(dup_path)

    basepath = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 145/HUB/HUB-event10-9-12/'
    # dir_lister = DirLister(basepath)
    # dir_lister.report()

    ddl = DupDirLister(basepath, dup_path)
    # ddl.report()



    if 0: # dup test
        path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 22/Washington_Warren/washington6.tif'
        dups = dup_mgr.find_dups_for_file(path)
        print dups

        checksum = '0042e240dcdf2ff62c0205ed68250a0c'
        dups = dup_mgr.find_dups_for_checksum(checksum)
        print dups

    import re
    disc_pat = re.compile ("CIC-ExternalDisk1/disc ([0-9]+)")
    foo = "/asdfsdf/CIC-ExternalDisk1/disc 111/asdfasdf/asdfasdf"
    m = disc_pat.search(foo)
    if m:
        print 'found - {}'.format(m.group(1))
        print dir (m)
    else:
        print 'NOPE'