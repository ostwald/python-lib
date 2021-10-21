"""
experiment with filtering unwanted comms_files from databases
"""

import os, sys, re
import sqlite3
import globals
from comms_db import CommsDBTable

class SqlFilter:

    path_frag_filter = map (lambda x:x.lower(), globals.SKIP_DIR_NAME_FRAGS + globals.SKIP_DIR_NAMES)
    min_size = '1000000'

    def __init__ (self, sqlite_file):
        self.sqlite_file = sqlite_file
        self.filter_clause = self.make_path_filter_clause()
        self.size_clause = "size > {}".format(self.min_size)

        self.filter_and_size_clause = self.filter_clause + " AND " + self.size_clause

        self.tail_clause = "FROM comms_files WHERE {}".format(self.filter_and_size_clause)

        conn = sqlite3.connect(self.sqlite_file)
        self.cursor = conn.cursor()

    def make_path_filter_clause (self):
        # q = "NOT (" + " OR ".join (map (lambda x:"LOWER(path) like '%{}%'".format(x), self.path_frag_filter)) + ")"
        q = "NOT (" + " OR ".join (map (lambda x:"LOWER(path) like '%{}%'".format(x), self.path_frag_filter)) + ")"
        return q

    def select_filtered (self):
        query = "SELECT * {}".format(self.tail_clause)

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        # return map(lambda x:x[0], rows)
        return rows

    def count_filtered (self):
        query = "SELECT COUNT(*) {}".format(self.tail_clause)

        self.cursor.execute(query)
        row = self.cursor.fetchone()
        # return map(lambda x:x[0], rows)
        return int(row[0])

    def sum_size_select_filtered(self):
        query = "SELECT SUM (size) {}".format(self.tail_clause)

        self.cursor.execute(query)
        row = self.cursor.fetchone()
        # return map(lambda x:x[0], rows)
        return int(row[0])

if __name__ == '__main__':
    # print path_frag_filter
    # print make_path_filter_clause(path_frag_filter)

    # sqlite_file = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk1/CIC-ExternalDisk1.sqlite'
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'

    sql_filter = SqlFilter(sqlite_file)

    print "SELECT * {}".format(sql_filter.tail_clause)

    if 1:
        rows = sql_filter.select_filtered ()
        print '{} rows selected'.format(len(rows))

    if 0:
        num = sql_filter.count_filtered ()
        print 'file count: {}'.format(num)

    if 0:
        size = sql_filter.sum_size_select_filtered ()
        # print 'sum size: {}M'.format(int(size/1000000))
        print 'sum size: {}'.format(size)

