import os

from comms_db import CommsDBTable

if 1:
    for disc_num in range(173,174):
        command = 'python dir_lister_utils.py {} > listings/disc_{}.txt'.format(disc_num, disc_num)
        # command = 'python dir_lister.py \'{} \' > listings/disc_{}.txt'.format(disc_num, disc_num)
        print command
        os.system(command)
        print  ' ... done'

if 0:
    base_dir = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1'
    for filename in os.listdir(base_dir):
        if filename.startswith('disc 87'):
            print '"{}"'.format(filename)
            for i, ch in enumerate(filename):
                print '- {} - {} ({})'.format(i, ch, ord(ch))

if 0:  #hard coded
    # command = 'python dir_lister.py \'87 \' > listings/disc_87.txt'
    command = 'python dir_lister.py 134b > listings/disc_134b.txt'
    print command
    os.system(command)
    print  ' ... done'


if 0: # comms video loader
    from db_loader import AutoLoader
    db_root = '/Users/ostwald/Documents/comms-video'

    loader = AutoLoader()
    loader.process()

if 0:

    class Normalizer:

        def __init__ (self, sqlite_file):
            self.sqlite_file = sqlite_file
            self.db = CommsDBTable(self.sqlite_file)