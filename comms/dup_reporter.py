import sys, os, re
from dup_manager import DupManager
from comms_db import CommsDBTable
import globals



FIELD_PROJECT_PATH = '/Volumes/archives/CommunicationsImageCollection/Field Projects'
DEDUP_FIELD_PROJECT_PATH = '/Volumes/cic-de-duped/Field Projects'
STAGING_PATH = '/Volumes/archives/CommunicationsImageCollection/Staging'

class DupReporter (DupManager):

    accept_pat = None
    stop_phrases = ["IMG", "CR2", 'jpg', 'tif','tiff', "JPG",]
    sqlite_file = globals.composite_sqlite_file

    def accept (self, s):
        """
        return True if this filename contains a "name" (see self.accept_pat),
        AND if that name does not contain any of the stop phrases
        :param s:
        :return:
        """
        for stop_phrase in self.stop_phrases:
            s = s.replace (stop_phrase, '')

        if self.accept_pat is not None:
            m = self.accept_pat.search (s)
            if not m:
                return False

        return True

    def __init__ (self, dup_data_path):
        self.db = None
        if self.sqlite_file is not None:
            self.db = CommsDBTable(self.sqlite_file)
        DupManager.__init__(self, dup_data_path)
        self.size = len (self.dup_map.keys())

    def report_dupset (self, checksum):
        dupset = self.get_dupset(checksum=checksum)
        if dupset is None:
            print 'ERROR: dupset not found for {}'.format(checksum)
        print '\n{}'.format(dupset.checksum)
        for p in dupset.duplist:
            # asterisk = (p == dupset.file) and '*' or ''
            asterisk = os.path.exists(p) and '*' or ''
            print '- {}{}'.format(asterisk, p)

    def report (self):

        dup_map = self.dup_map
        checksums = dup_map.keys()

        print '{}\nPath: {}'.format('-'*60, self.data_path.replace ('/Users/ostwald/Documents/Comms/',''))
        print '{} dupsets'.format(len(checksums))

        # how many dup_items?
        dup_items = 0

        for cs in checksums:
            dupset = dup_map[cs]
            # self.report_dupset(cs)
            dup_items = dup_items + len (dupset)

        print '{} total dup ITEMS'.format(dup_items)

        staging_paths = self.find_dup_items_with_substring(STAGING_PATH)
        print '{} staging_DUP_paths found'.format(len(staging_paths))

        staging_non_dups = self.find_non_dups_for_directory (STAGING_PATH, self.sqlite_file)
        print '{} staging_NON_dups found'.format(len(staging_non_dups))

        # self.report_staging_dups_to_delete()
        # self.process_People_HAO_sets()
        self.process_staging_dups_short_path()

    def process_People_HAO_sets (self):
        """
        process
        :param dup_manager:
        :return:
        """
        dup_map = self.dup_map
        checksums = self.dup_map.keys()
        to_delete = []
        people_dup_sets = []
        print ' - there are {} dup sets total'.format(len(checksums))
        for i, key in enumerate(checksums):
            people_paths = []
            non_people_paths = []
            paths = dup_map[key]
            for path in paths:
                if "People HAO CSBF" in path:
                    people_paths.append (path)
                else:
                    non_people_paths.append (path)
                    # print path

            if len (people_paths) == 0:
                continue

            people_dup_sets.append(key)
            if len (people_paths) > 1:
                print '{} people paths!'.format(len(people_paths))

            keeper = people_paths[0]

            print '\n{}'.format(key)
            for p in people_paths:
                if p == keeper:
                    asterisk = '*'
                else:
                    asterisk = ' '
                    to_delete.append(p)
                print ' - {} {}'.format(asterisk, p[1:])
            for p in non_people_paths:
                print ' -    {}'.format(p[1:])
                to_delete.append(p)



        print 'total to delete: {}'.format(len(to_delete))


        print '{} people dupsets will be eliminated'.format(len(people_dup_sets))


        if 0: # Do the delete
            cnt_to_delete = len(to_delete)
            for i, path in enumerate(to_delete):
                if i % 100 == 0:
                    print '- {}/{} - {}'.format(i, cnt_to_delete,path[1:])
                try:
                    self.db.delete_record ("path = '{}'".format(path))
                except:
                    print 'delete_record ERROR: {}'.format(sys.exc_info())


    def process_staging_dups_short_path (self):
        """
        keep the shortest path and delete the others

        :param dup_manager:
        :return:
        """
        dup_map = self.dup_map
        checksums = self.dup_map.keys()
        to_delete = []
        print ' - there are {} dup sets total'.format(len(checksums))

        for i, key in enumerate(checksums):
            paths = dup_map[key]
            shortest = None

            for path in paths:
                if shortest is None:
                    shortest = path
                elif len(path) < len(shortest):
                    shortest = path
                keeper = shortest



            print '\n{}'.format(key)
            for p in paths:
                if p == keeper:
                    asterisk = '*'
                else:
                    asterisk = ' '
                    to_delete.append(p)
                print ' - {} {}'.format(asterisk, p[1:])

        print 'total to delete: {}'.format(len(to_delete))

        for p in to_delete:
            print '-', p

        if 1: # Do the delete
            cnt_to_delete = len(to_delete)
            for i, path in enumerate(to_delete):
                if i % 100 == 0:
                    print '- {}/{} - {}'.format(i, cnt_to_delete,path[1:])
                try:
                    self.db.delete_record ("path = '{}'".format(path.replace ("'", "''")))
                except:
                    print 'delete_record ERROR: {}'.format(sys.exc_info())



    def process_staging_same_filename_sets (self):
        """
        process
        :param dup_manager:
        :return:
        """
        dup_map = self.dup_map
        checksums = self.dup_map.keys()
        to_delete = []
        same_name_sets = []
        print ' - there are {} dup sets total'.format(len(checksums))
        for i, key in enumerate(checksums):
            stagers = []
            file_names = []
            non_stagers = []
            paths = dup_map[key]
            for path in paths:
                if path.startswith (STAGING_PATH):
                    stagers.append (path)
                    file_name = os.path.basename (path)
                    if file_name not in file_names:
                        file_names.append(file_name)
                else:
                    non_stagers.append (path)
                    # print path

            if len (non_stagers) > 0:
                continue

            if len(file_names) == 1:
                same_name_sets.append (key)
                shortest = None
                for path in stagers:
                    if shortest is None:
                        shortest = path
                    elif len(path) < len(shortest):
                        shortest = path
                keeper = shortest

                print '\n{}'.format(key)
                for p in stagers:
                    if p == keeper:
                        asterisk = '*'
                    else:
                        asterisk = ' '
                        to_delete.append(p)
                    print ' - {} {}'.format(asterisk, p[1:])


        print '\n{} same name sets'.format(len(same_name_sets))

        print 'total to delete: {}'.format(len(to_delete))


        if 0: # Do the delete
            cnt_to_delete = len(to_delete)
            for i, path in enumerate(to_delete):
                if i % 100 == 0:
                    print '- {}/{} - {}'.format(i, cnt_to_delete,path[1:])
                try:
                    self.db.delete_record ("path = '{}'".format(path))
                except:
                    print 'delete_record ERROR: {}'.format(sys.exc_info())


    def report_staging_dups_to_delete (self):
        """
        for each dup set, if there is at least one member NOT from Staging, the delete the dups from Staging.
        :param dup_manager:
        :return:
        """
        dup_map = self.dup_map
        checksums = self.dup_map.keys()
        to_delete = []
        print ' - there are {} dup sets total'.format(len(checksums))
        for i, key in enumerate(checksums):
            stagers = []
            non_stagers = []
            paths = dup_map[key]
            for path in paths:
                if path.startswith (STAGING_PATH):
                    stagers.append (path)
                else:
                    non_stagers.append (path)
                    # print path

            if len (non_stagers) > 0:
                to_delete = to_delete + stagers

                if 0: # verbose
                    print '\n{}'.format(key)
                    for p in non_stagers:
                        print '-',p[1:]
                    for p in stagers:
                        print 'x', p[1:]

        to_delete.sort()
        cnt_to_delete = len (to_delete)
        print 'To Delete ({})'.format(cnt_to_delete)

        if 0: # Do the delete

            for i, path in enumerate(to_delete):
                if i % 100 == 0:
                    print '- {}/{} - {}'.format(i, cnt_to_delete,path[1:])
                try:
                    self.db.delete_record ("path = '{}'".format(path))
                except:
                    print 'delete_record ERROR: {}'.format(sys.exc_info())


if __name__ == '__main__':

    dups_file = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'
    # dups_file = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'
    # dups_file = '/Users/ostwald/Documents/Comms/Composite_DB/versions/small Staging (bog)/master_check_sum_dups.json'
    reporter = DupReporter(dups_file)
    reporter.report()


    # paths = reporter.find_paths()
    # print "there are {} paths total".format(len(paths))
