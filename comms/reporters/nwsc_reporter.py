"""
From Holly:
Laura and I were wondering if you could (easily) generate a spreadsheet for the NWSC folders on discs 137-143,
for what is currently on de-duped?  We thought this might help me eyeball what remains, and be able to re-order
it visually for a better comparison.

If there were columns for disc number, folder name, and image numbers, that's all I'd need.   (note one folder has a
typo in the name, it says MWSC, please include that one.

"""
import os, sys, re
from comms.dir_lister import DirLister
from UserList import UserList

class NWSCLister (UserList):

    def __init__ (self, disc_dir):
        self.data = []
        self.disc_dir = disc_dir
        self.disc_name = os.path.basename(disc_dir)
        for filename in os.listdir(self.disc_dir):
            path = os.path.join (self.disc_dir, filename)
            # print path
            if os.path.isdir(path) and 'NWSC' in filename or 'MWSC' in filename:
                self.list_folder(path)

    def list_folder (self, path):
        print 'list_folder', path
        img_listing = DirLister(path, recursive=0).list_img_spans()
        rel_path = path.replace(self.disc_dir, '')
        self.data.append ([self.disc_name, rel_path, img_listing])

        for filename in os.listdir(path):
            item_path = os.path.join(path, filename)
            if os.path.isdir(item_path):
                self.list_folder(item_path)

if __name__ == '__main__':
    rows = []
    rows.append (['disc', 'folder', 'image numbers'])
    for disc_num in range(138, 139):  #144
        print disc_num
        disc_path = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc {}'.format(disc_num)
        lister = NWSCLister(disc_path)
        for row in lister.data:
            rows.append(row)

    out_path = 'NWSC_REPORT_2.tsv'
    fp = open (out_path, 'w')
    fp.write ('\n'.join (map (lambda x:'\t'.join(x), rows)))
    fp.close()
    print 'wrote to', out_path