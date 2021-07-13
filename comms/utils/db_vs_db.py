"""
compares 2 DBs
"""

import os, sys
import comms.globals
from comms.comms_db import CommsDBTable

class DB_Comparator:

    def __init__ (self, sqlite_A, sqlite_B):
        self.sqlite_A = sqlite_A
        self.sqlite_B = sqlite_B
        self.db_A = CommsDBTable(sqlite_A)
        self.db_B = CommsDBTable(sqlite_B)

    def report (self):
        sort_spec = 'path ASC'
        items_A = self.db_A.select_all_records(sort_spec)
        items_B = self.db_B.select_all_records(sort_spec)

        print 'there are {} items in {}'.format(len(items_A), self.sqlite_A)
        print 'there are {} items in {}'.format(len(items_B), self.sqlite_B)

        paths_A = map (lambda x:x[1].replace('/Volumes/archives/CommunicationsImageCollection/',''), items_A)
        paths_B = map (lambda x:x[1].replace('/Volumes/cic-de-duped/',''), items_B)

        print '\nPaths in {} that are not in {}'.format(self.sqlite_A, self.sqlite_B)
        for path in paths_A:
            if not path in paths_B:
                print '- {}'.format(path)


        print '\nPaths in {} that are not in {}'.format(self.sqlite_B, self.sqlite_A)
        for path in paths_B:
            if not path in paths_A:
                print '- {}'.format(path)

if __name__ == '__main__':
    sqlite_A = '/Users/ostwald/Documents/Comms/Composite_DB/field_projects_duped.sqlite'
    sqlite_B = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'

    cmp = DB_Comparator(sqlite_A, sqlite_B)
    cmp.report()
