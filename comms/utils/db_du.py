"""
Simulate the unix "du" call using
"""
import os, sys
from comms import CommsDBTable
import sqlite3

class DU:

    def __init__ (self, sqlite_file, root_dir):
        self.db = CommsDBTable(sqlite_file)
        self.root_dir = root_dir

        for subdir in self.db.list_dir(self.root_dir):
            path = os.path.join (root_dir, subdir)
            size = self.get_size (path)
            print '{}\t{}'.format(human_readable_size(size), subdir)

        total_size =  self.get_size (root_dir)
        print human_readable_size(total_size)

    def get_size (self, path):
        # conn = sqlite3.connect(self.db.sqlite_file)
        # c = conn.cursor()
        #
        # query = "SELECT SUM (size) FROM comms_files WHERE path LIKE '{}%'".format(path)
        # print query
        # c.execute(query)
        # return c.fetchone()[0]
        if 0 and os.path.isfile(path):
            rows = self.db.select ('size', "WHERE path='{}'".format(path))
            print rows
            return rows[0][0]
        return self.db.sum_size_for_selected ("WHERE path LIKE '{}%'".format(path))

def human_readable_size(s):

    n = None
    try:
        n = int(s)
    except:
        n = 0

    if n < 1000000:
        return '{}K'.format(n/1000)
    if n < 1000000000:
        return '{}M'.format(n/1000000)
    else:
        return '{}G'.format(n/1000000000)

def get_size (path):
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    db = CommsDBTable(sqlite_file)
    rec = db.select ('size', "WHERE path='{}'".format(path))
    print rec[0][0]

def du_deduped_field_projects():
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    root_dir = '/Volumes/cic-de-duped/Field Projects'
    # root_dir = '/Volumes/cic-de-duped/Field Projects/Field Project-DC3-FP22/Disc 1/jpgs'
    DU(sqlite_file, root_dir)

def du_original_stage():
    sqlite_file = '/Users/ostwald/Documents/Comms/Staging/Staging.sqlite'
    root_dir = '/Volumes/archives/CommunicationsImageCollection/Staging'
    DU(sqlite_file, root_dir)

if __name__ == '__main__':
    du_deduped_field_projects()
    # du_original_stage()
    # get_size ('/Volumes/cic-de-duped/Field Projects/Field Project-DC3-FP22/Disc 1/jpgs/_MG_1739sm.jpg')