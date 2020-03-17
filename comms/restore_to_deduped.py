"""

Holly has provided a file with directory paths, one per line

For each directory, we want to find the original files that match
the de-duped version of the raws for that directory, and restore from
original to de-duped directory

"""
import os, sys, re, shutil
from comms_db import CommsDBTable



class Restorer:

    de_dup_db_file = '/Users/ostwald/Documents/Comms/Composite_DB/versions/cic-de-duped.sqlite'
    comms_images_base = '/Volumes/archives/CommunicationsImageCollection'
    de_duped_base = '/Volumes/cic-de-duped'

    def __init__ (self):
        self.db = CommsDBTable(self.de_dup_db_file)

    def restore_dir(self, frag):
        de_dup_dir = self.get_restore_dir(frag)
        print '\nde_dup_dir: ', de_dup_dir
        for filename in self.db.list_dir(de_dup_dir):
            root, ext = os.path.splitext(filename)
            # print root, ext
            if not ext in ['.CR2', '.CRW']:
                continue
            print '- {}'.format(filename)

            de_dup_path = os.path.join (de_dup_dir, filename)
            original_path = os.path.join (self.get_original_dir(frag), filename)

            if os.path.exists (de_dup_path):
                print '      de_dup_path SHOULD NOT exist at {}'.format(de_dup_path)
                continue

            if not os.path.exists (original_path):
                print '      original_path SHOULD exist at {}'.format(original_path)
                continue

            try:
                shutil.copy2(original_path, de_dup_path)
                print '      ... copied'
            except Exception, msg:
                print 'ERROR: {}'.format(msg)
                sys.exit(1)


    def normalize_pc_name (self, pc_name):
        """

        :param pc_name: e.g., "PC-2"
        :return:
        """

        return pc_name.replace('PC-', 'disc ')

        # pat = re.compile('PC\-([0-9]*)')
        # m = pat.match (pc_name)
        # if m:
        #     print 'MATCH'
        #     return 'disc {}'.format(m.group(1))
        # else:
        #     print 'no match'

    def get_restore_list (self):
        path = '/Users/ostwald/devel/python-lib/comms/reports/restore raw list.txt'
        lines = map (lambda x:x.strip(), open(path, 'r').read().split('\r'))
        lines = filter (lambda x:len(x)>0, lines)
        print '{} paths read'.format(len (lines))
        return map (lambda x:self.normalize_pc_name(x), lines)

    def get_restore_dir (self, restore_frag):
        de_duped_path = '{}/CIC-ExternalDisk1/{}'.format(self.de_duped_base,self.normalize_pc_name(restore_frag))
        # print 'de_duped_path: {}'.format(de_duped_path)
        return de_duped_path

    def get_original_dir (self, restore_frag):
        original_path = '{}/CIC-ExternalDisk1/{}'.format(self.comms_images_base,self.normalize_pc_name(restore_frag))
        # print 'original_path: {}'.format(original_path)
        return original_path

    def report_frag (self, frag):
        original = self.get_original_dir(frag)
        de_duped = self.get_restore_dir(frag)

        print '\nfrag: {}'.format(frag)
        print ' - original: {} - exists? {}'.format(original, os.path.exists(original))
        print ' - de_duped: {} - exists? {}'.format(de_duped, os.path.exists(de_duped))


if __name__ == '__main__':

    restorer = Restorer()
    paths = restorer.get_restore_list()


    if 1:
        for p in paths:
            # print '{} ({})'.format(p, len(p))
            # restorer.report_frag (p)
            restorer.restore_dir (p)

    if 1:
        frag = paths[1]
        restorer.restore_dir(frag)