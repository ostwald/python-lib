"""
save output of dupfinder to disk
"""
import os, traceback
from dup_finder import DupFinder
# REPORT_BASE_DIR = '/Users/ostwald/Documents/Comms/dup_reports/Staging'
# ARCHIVE_BASE_PATH = '/Volumes/archives/CommunicationsImageCollection/Staging'

REPORT_BASE_DIR = '/Users/ostwald/Documents/Comms/dup_reports/ExternalDisk1'
ARCHIVE_BASE_PATH = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1'

DUP_DATA_PATH = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'

class DupReporter (DupFinder):

    def get_dup_display_path (self, dup_path):
        default_base_dup_display = os.path.join(self.base_dedup_path, 'CIC-ExternalDisk1/')
        if dup_path.startswith (default_base_dup_display):
            return dup_path.replace(default_base_dup_display, 'CIC-ExternalDisk1/')
        else:
            return dup_path.replace (self.base_dedup_path, '')

    def report_dir (self, dir_path):
        """
        if there are files (not .DS_Store) report dups
        if there are dirs, call report_dir recursively

        :param dir_path:
        :return:
        """

        files = []
        directories = []
        for filename in os.listdir(dir_path):
            if filename[0] == '.' or filename.endswith('.xmp'): continue
            path = os.path.join (dir_path, filename)
            if os.path.isfile (path):
                files.append(path)
            else:
                directories.append(path)
        if len(files) > 0:
            self.report_dups (dir_path)
        for directory in directories:
            self.report_dir (directory)


    def report_dups (self, dir_path):
        """
        print a list of duplicates, the one which exists on disk is marked with an asterisk
        :param dir_path: The (Archives-based) path to the directory to be reported
        :return:
        """

        print 'dir_path:', dir_path
        segments = dir_path.split('/')
        rel_segments = segments[len(ARCHIVE_BASE_PATH.split('/')):]
        rel_report_path = '/'.join(rel_segments) + '.txt'
        report_path = os.path.join (REPORT_BASE_DIR, rel_report_path)

        if not os.path.exists(os.path.dirname(report_path)):
            os.makedirs(os.path.dirname(report_path))
        if os.path.exists(report_path):
            print 'skipping {} - already exists'.format(report_path)
            return

        report_lines = [];add=report_lines.append
        print len(os.listdir(dir_path)), 'in archive directory'
        dupset = self.find_dups_for_directory (dir_path)
        keys = dupset.keys()
        if len(keys) == 0:
            return
        keys.sort()
        print '- ', len(keys), 'dups found'
        add ('- {} dups found'.format(len(keys)))
        cnt = 0
        for key in keys:
            dedup_key_path = self.make_deduped_path(key)
            print '\n', '{}{}'.format(self.get_dup_display_path(dedup_key_path), os.path.exists(dedup_key_path) and ' *' or '')
            add ('\n{}{}'.format(self.get_dup_display_path(dedup_key_path), os.path.exists(dedup_key_path) and ' *' or ''))
            dups = dupset[key]
            for dup in dups:
                dedup_path = self.make_deduped_path(dup)
                print ' - {}{}'.format(self.get_dup_display_path(dedup_path), os.path.exists(dedup_path) and ' *' or '')
                add (' - {}{}'.format(self.get_dup_display_path(dedup_path), os.path.exists(dedup_path) and ' *' or ''))

            cnt += 1
            if cnt > 5000:
                break

        fp = open(report_path, 'w')
        fp.write ('\n'.join(report_lines))
        fp.close()
        print 'wrote', report_path

def report_paths_for_checksum(checksum):
    finder = DupReporter(DUP_DATA_PATH)
    for path in finder.find_dups_for_checksum(id):
        print finder.make_deduped_path(path)

def report_dir (rel_path):
    finder = DupReporter (DUP_DATA_PATH)
    dir_path = os.path.join (ARCHIVE_BASE_PATH, rel_path)
    print 'DIR_PATH:', dir_path
    finder.report_dir(dir_path)

def count_photo_dups ():
    finder = DupReporter (DUP_DATA_PATH)
    dupsets = finder.find_dups_with_substring('CIC-ExternalDisk1/photos')
    print len(dupsets), 'dupsets found'
    return dupsets

def count_photo_items ():
    finder = DupReporter (DUP_DATA_PATH)
    paths = finder.find_dup_items_with_substring('CIC-ExternalDisk1/photos')
    print len(paths), 'items found'
    return paths

if __name__ == '__main__':
    # path = 'Field Project-PECAN-FP20'
    finder = DupReporter (DUP_DATA_PATH)
    path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos'
    finder.report_dir (path)

    # id = 'c8abc3c500f0ff99f352c4173402ae78'
    # report_paths_for_checksum(id)


