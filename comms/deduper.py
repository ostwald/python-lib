"""
on a copy of composite:
- for all dup groups containing at least one dup on ExternalDisk1:
 - delete non-ExternalDisk1 items
   - if there is a single dup from a disc #, keep only that one

"""
import os,sys,json, re
import globals
from dup_analysis import DupAnalyzer
from comms_db import CommsDBTable
from sql_filter import SqlFilter
import sqlite3

class Reaper(DupAnalyzer):

    def __init__ (self, dup_data_path, sqlite_file):
        DupAnalyzer.__init__(self, dup_data_path)
        self.db = CommsDBTable(sqlite_file)


    def delete_record (self, path):
        try:
            self.db.delete_record ("path = '{}'".format(path))
        except:
            print 'delete_record ERROR: {}'.format(sys.exc_info())

    def select_record (self, path):
        conn = sqlite3.connect(self.db.sqlite_file)
        c = conn.cursor()

        query = "SELECT * from {} WHERE path = '{}'".format(self.db.table_name, path)

        c.execute(query)
        rows = c.fetchall()
        # return map(lambda x:x[0], rows)
        return rows

    def filter_by_paths (self):
        """
        using the paths defined in globals, delete all images from relavant paths

        this is only necessary if global paths have changed since database was created
        """
        path_frag_filter = map (lambda x:x.lower(), globals.SKIP_DIR_NAME_FRAGS + globals.SKIP_DIR_NAMES)
        clause = "(" + " OR ".join (map (lambda x:"LOWER(path) like '%{}%'".format(x), path_frag_filter)) + ")"

        print clause

        conn = sqlite3.connect(self.db.sqlite_file)
        c = conn.cursor()
        query = "DELETE from {} WHERE {}".format(self.db.table_name, clause)

        c.execute(query)
        print 'records affected: {}'.format(conn.total_changes)
        conn.commit()

    def dedup_1 (self):
        """
        the dup_sets found by find_disk_1_dups all have at least one ExternalDisk1 version
        - first delete the
        :return:
        """
        dup_sets = self.find_disk_1_dups()

        disc_pat = re.compile ("CIC-ExternalDisk1/disc [0-9]*")

        for key in dup_sets:

            disc_pat_keepers = [] # these match disc_pat
            other_keepers = []  # these just have CIC-ExternalDisk1
            others = []

            # print all in the set
            print '\n{}'.format(key)
            for path in self.dup_map[key]:
                print '- {}'.format(path)
                if self.is_ignorable (path): continue
                if disc_pat.search(path):
                    disc_pat_keepers.append(path)
                elif 'CIC-ExternalDisk1' in path:
                    other_keepers.append (path)
                else:
                    others.append(path)

            to_keep = None

            if len(disc_pat_keepers) > 0:
                to_keep = disc_pat_keepers
                print "\n  disc_pat_keepers"
                for p in disc_pat_keepers:
                    print '  -', p

            elif len(other_keepers) > 0:
                to_keep = other_keepers

                print "\n  other keepers"
                for p in other_keepers:
                    print '  -', p

            elif len(others) > 0:
                to_keep = others
                print "\n  others"
                for p in others:
                    print '  -', p

            else:
                print '\n  WARN: No Keepers found for {}'.format(key)


            if to_keep is not None:
                print '\n  To Delete'
                for path in self.dup_map[key]:
                    if not path in to_keep:
                        print '     x', path
                        # self.delete_record (path)

    def dedup_2 (self):
        """
        We are looking for chances to delete non-CIC-ExternalDisk1 dups. So if there is
        a CIC-ExternalDisk1, then delete all the non-CIC-ExternalDisk1 dups in the dupset
        """
        dup_sets = self.find_disk_1_dups()

        disc_pat = re.compile ("CIC-ExternalDisk1/disc [0-9]*")

        total_to_delete = 0

        for key in dup_sets:

            externalDisk1_dups = [] # these contain CIC-ExternalDisk1
            other_dups = []  # these do NOT have CIC-ExternalDisk1

            # print all in the set
            print '\n{}'.format(key)
            for path in self.dup_map[key]:
                print '- {}'.format(path)
                if "CIC-ExternalDisk1/" in path:
                    externalDisk1_dups.append (path)
                else:
                    other_dups.append(path)

            if len(other_dups) > 0 and len(externalDisk1_dups) > 0:
                print '\n - to delete'
                for dup in other_dups:
                    print '  -', dup
                    total_to_delete += 1
                    self.delete_record (dup)

        print 'total to delete: {}'.format(total_to_delete)


    def is_ignorable (self, path):
        ignorables = [
            'design and work files',
            'work files',
            'work files restore',
            'ignore these',
            'need to be archived'
        ]
        for i in ignorables:
            if i in path:
                return 1
        return 0

if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'
    dup_data = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'


    reaper = Reaper (dup_data, sqlite_file)
    # reaper.filter_by_paths()
    reaper.dedup_2()
