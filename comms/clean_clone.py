"""
clean clone a given database - meaning that the new (clone) will not have any dups
"""
import os, sys
from comms_db import CommsDBTable
from dup_manager import DupManager
import sqlite3
import globals



class CleanCloner:

    def __init__ (self, sqlite_file, dup_data, clean_sqlite_file):
        self.sqlite_file = sqlite_file
        self.dup_data = dup_data
        self.clean_sqlite_file = clean_sqlite_file

        if os.path.exists (self.clean_sqlite_file):
            os.remove (self.clean_sqlite_file)

        self.clean_db = CommsDBTable(self.clean_sqlite_file)
        self.source_db = CommsDBTable(self.sqlite_file)
        self.dups =  DupManager(self.dup_data)

    def clone (self):
        src_records = self.source_db.select_all_records()
        for i, rec in enumerate(src_records):
            path = rec[1]

            if not self.clean_db.count_selected("WHERE path = '{}'".format(globals.normalize_db_path(path))) > 0:
                self.add_record(rec)

            if i > 1 and i % 1000 == 0:
                print '{}/{}'.format(i, len(src_records))

        print 'cloned'

    def add_record (self, row):
        conn = sqlite3.connect(self.clean_sqlite_file)
        c = conn.cursor()

        row = list(row)

        row[1] = globals.normalize_db_path(row[1])
        print row

        # quoted_schema = ','.join(map (lambda x:"'%s'" % x, HOSTS_SCHEMA_SPEC))
        quoted_schema = self.clean_db.schema.quoted_schema

        # put data list together to match with schema fields
        quoted_values = ','.join(map (lambda x:u"'{}'".format(x), row))  # current

        try:
            c.execute("INSERT INTO {tn} ({fn}) VALUES ({fv})" \
                      .format(tn=self.clean_db.table_name, fn=quoted_schema, fv=quoted_values.encode('utf8')))
        except:
            print 'quoted_values is a {}'.format(type(quoted_values))
            print quoted_values
            print('ERROR: {}'.format(sys.exc_info()))
            traceback.print_stack()
            sys.exit()

        conn.commit()
        conn.close()


if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    dup_data = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped-reports/dups/check_sum_dups.json'
    clean_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped-CLEAN.sqlite'


    cloner = CleanCloner(sqlite_file, dup_data, clean_sqlite_file)
    cloner.clone()