"""
help find Holly find dups in the PC's

Given a particular dir - report the dupset of each of the files so we can see
where the dups are

"""
import os, sys, re

from comms.dup_manager import DupManager

class DupFinder (DupManager):

    base_archives_path = '/Volumes/archives/CommunicationsImageCollection/'
    base_dedup_path = '/Volumes/cic-de-duped/'

    def __init__ (self, dup_data_path):
        DupManager.__init__ (self, dup_data_path)

    def make_deduped_path (self, archive_path):
        # return archive_path
        rel_dedup_path = archive_path.replace (self.base_archives_path, '')
        # Kludge for Stage / Field Projects
        if rel_dedup_path.startswith('Staging'):
            rel_dedup_path = rel_dedup_path.replace('Staging', 'Field Projects')

        return os.path.join (self.base_dedup_path, rel_dedup_path)

    def make_archives_path (self, dedup_path):
        rel_archives_path = dedup_path.replace (self.base_dedup_path, '')
        # Kludge for Stage / Field Projects
        if rel_archives_path.startswith('Field Projects'):
            rel_archives_path = rel_archives_path.replace('Field Projects', 'Staging')

        return os.path.join (self.base_archives_path, rel_archives_path)

    def find_dups (self, dir_path):
        return self.find_dups_for_file(dir_path)

    def find_dups_for_directory (self, dirpath):
        dupset ={}
        for filename in self.list_dir(dirpath):
            path = os.path.join(dirpath, filename)
            dups = self.find_dups (path)
            if dups:
                dupset[path] = dups
        return dupset

    def get_dup_display_path (self, dup_path):
        default_base_dup_display = os.path.join(self.base_dedup_path, 'CIC-ExternalDisk1/')
        if dup_path.startswith (default_base_dup_display):
            return dup_path.replace(default_base_dup_display, '')
        else:
            return dup_path.replace (self.base_dedup_path, '')

    def report_dir (self, dir_path):
        """
        print a list of duplicates, the one which exists on disk is marked with an asterisk
        :param dir_path: The path to the directory to be reported
        :return:
        """
        print len(os.listdir(dir_path)), 'in archive directory'
        dupset = self.find_dups_for_directory (dir_path)
        keys = dupset.keys()
        keys.sort()
        print '- ', len(keys), 'dups found'
        for key in keys:
            # print '\n', key.replace(archives_base_path, '')
            dedup_key_path = self.make_deduped_path(key)
            # print '\n', '{}{}'.format(dedup_key_path, os.path.exists(dedup_key_path) and ' *' or '')
            print '\n', '{}{}'.format(self.get_dup_display_path(dedup_key_path), os.path.exists(dedup_key_path) and ' *' or '')
            dups = dupset[key]
            for dup in dups:
                dedup_path = self.make_deduped_path(dup)
                # print ' - {}{}'.format(dedup_path, os.path.exists(dedup_path) and ' *' or '')
                print ' - {}{}'.format(self.get_dup_display_path(dedup_path), os.path.exists(dedup_path) and ' *' or '')

    def list_dir (self, frag):
        if frag[0] == '/':
            path = frag
        else:
            # path = os.path.join(base_path, frag)
            path = os.path.join(self.base_dedup_path, frag)

        print 'PATH: ', path
        return os.listdir (path)

if __name__ == '__main__':


    # base_path = '/Volumes/archives/CommunicationsImageCollection/Staging'
    # filepath = os.path.join (archive_base_path, rel_path)

    if 0: # search under CIC-ExternalDisk1
        archive_base_path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1'
        deduped_base_path = None # default
        rel_path = 'disc 182/Emily CoBabe Ammann'

    if 0:  # search under field projects
        archive_base_path = '/Volumes/archives/CommunicationsImageCollection/Staging'
        deduped_base_path = '/Volumes/cic-de-duped/Field Projects'
        rel_path = 'Field Project-HIAPER-FP2/HIAPER 8-19-05/8-19-05'
        rel_path = 'Field Project-HIAPER-FP2/HIAPER 8-19-05/8-19-05/tif&jpgs'

    if 1:  # search under field projects
        archive_base_path = '/Volumes/archives/CommunicationsImageCollection/Staging'
        rel_path = 'SOARS-3/SOARS 11-1/HIRO-mentors'
        rel_path = 'Field Project-ARISTO-FP21/jpgs'

    dup_data_path = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'
    print dup_data_path
    # finder = DupFinder (dup_data_path, archive_base_path, deduped_base_path)
    finder = DupFinder (dup_data_path)
    dir_path = os.path.join (archive_base_path, rel_path)
    print 'DIR_PATH:', dir_path
    finder.report_dir(dir_path)

    if 0:  # test some paths
        path = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc 19/HIAPER take-off/8-19-05/tif&jpgs/IMG_5820.tif'
        print finder.make_deduped_path (path)

        path ='/Volumes/archives/CommunicationsImageCollection/Staging/Field Project-HIAPER-FP2/HIAPER Backups/HIAPER 2/HIAPER take-off/8-19-05/jpgs/IMG_5820.jpg'
        print finder.make_deduped_path(path)
