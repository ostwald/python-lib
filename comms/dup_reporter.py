import sys, os, re
from dup_manager import DupManager, filter_dup_paths, filter_dup_sets
from comms_db import CommsDBTable
import globals
from UserList import UserList
from comms.utils import DupFinder


# FIELD_PROJECT_PATH = '/Volumes/archives/CommunicationsImageCollection/Field Projects'
# DEDUP_FIELD_PROJECT_PATH = '/Volumes/cic-de-duped/Field Projects'
# STAGING_PATH = '/Volumes/archives/CommunicationsImageCollection/Staging'

class DupSet (UserList):

    def __init__ (self, key, mgr):
        self.key = key
        self.mgr = mgr
        self.data = self.mgr.dup_map[key]
        # self.__len__ = len(self.data)

    def __repr__ (self):
        return '\n'.join(self.data)

class DupReporter (DupManager):

    sqlite_file = globals.composite_sqlite_file
    # sqlite_file = '/Users/ostwald/Documents/Comms/Stragglers/composite-merged.sqlite'

    def __init__ (self, dup_data_path):
        self.db = None
        if self.sqlite_file is not None:
            self.db = CommsDBTable(self.sqlite_file)
        DupManager.__init__(self, dup_data_path)
        self.size = len (self.dup_map.keys())

    def report (self):

        dup_map = self.dup_map
        checksums = dup_map.keys()

        print '{}\nPath: {}'.format('-'*60, self.data_path.replace ('/Users/ostwald/Documents/Comms/',''))
        print '{} dupsets'.format(len(checksums))
        path_map = self._get_path_map()
        print '{} paths mapped'.format(len(path_map.keys()))

    def report_long_fp_dupsets(self):
        field_project_keys = self.find_dups_with_substring("soars")
        dupsets = map (lambda x:DupSet(x, self), field_project_keys)

        # dupsets = filter (lambda x:len(x)>2, dupsets)
        print len(dupsets), 'long field project dupsets'

        for ds in dupsets:
            print '{}\n'.format(ds)

if __name__ == '__main__':
    import dup_manager
    # dups_file = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'
    dups_file = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'

    reporter = DupFinder(dups_file)

    # find all dupsets with a Field Project member
    # def filter_fn(path):
    #     if ('CIC-ExternalDisk1/photos' in path or '/Field Projects/' in path or '/Staging/'in path):
    #         return 0
    #     else:
    #         return 1
    #
    # paths = filter_dup_paths(reporter, filter_fn)
    # print len(paths), 'found'

    def dup_set_filter (checksum):
        duplist = reporter.find_dups_for_checksum(checksum)
        fp_paths = []
        photos_paths = []
        other_paths = []
        for path in duplist:
            if '/Volumes/archives/CommunicationsImageCollection/Staging' in path:
                fp_paths.append (path)
            elif '/Volumes/archives/CommunicationsImageCollection/Field Projects' in path:
                fp_paths.append(path)
            elif '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos' in path:
                photos_paths.append(path)
            else:
                other_paths.append(path)
        if len(fp_paths) == 0:
            return 0
        if len(other_paths) == 0:
            return 0
        return 1

    dupsets = filter_dup_sets (reporter, dup_set_filter)
    print len(dupsets), 'dupsets after filter'

    if 1: # print results
        for checksum in dupsets:
            duplist = list (set (map (reporter.make_deduped_path, reporter.find_dups_for_checksum(checksum))))
            print checksum
            for path in duplist:
                exists =  os.path.exists(path) and '*' or ''
                print '- {} {}'.format(path, exists)
            print ''

    # now filter so that dupsets with only FieldProject and CIC-ExternalDisk1/photos items are eliminated
    # now filter dupsets where the file is in FieldProject

    # reporter.report()

