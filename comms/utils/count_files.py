"""
count the files in a directory tree
"""
import os
import traceback
import re

LOG_FILE = None

def write_log (s):
    fp = open(LOG_FILE, 'a')
    fp.write('\n')
    fp.write(s)
    fp.close()

def accept_dir_path(path):
    return 1
    if not path.startswith('/Volumes/cic-de-duped/CIC-ExternalDisk1/disc '):
        return False
    return True

def count_descendents(base_dir, recurse=False):
    # fp = open(LOG_FILE, 'wa')
    # fp.close()
    count = 0
    for child in os.listdir(base_dir):
        if child == '.DS_Store':continue
        child_path = os.path.join(base_dir, child)
        if os.path.isdir(child_path) and accept_dir_path (child_path) and recurse:
            count += count_descendents(child_path, recurse)
        elif os.path.isfile(child_path):
            count += 1

    print base_dir, count
    write_log ('{} - {}'.format(base_dir, count))
    return count

if __name__ == '__main__':

    # root = '/Volumes/cic-de-duped/CIC-ExternalDisk1'
    # root = '/Volumes/cic-de-duped/Field Projects'
    root = '/Volumes/cic-de-duped/CIC-ExternalDisk1/photos/1-archived/FP 22 DC3'
    log = '/Users/ostwald/Documents/Comms/logs'
    filename = 'count.txt'
    LOG_FILE = os.path.join(log,filename)
    descendents = count_descendents(root, True)
    print descendents, 'descendents'