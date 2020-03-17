"""
The composite database replaced quotes in paths with %27, which turns out not to be necessary.
This normalizer changes these paths back to match the paths on disk
"""
import os, sys, copy, traceback
from comms.comms_db import CommsDBTable
from comms.dup_manager import DupManager
import sqlite3
import comms.globals

class CompositeNormalizer:

    dowrites = 1

    def __init__ (self):
        self.sqlite_file = comms.globals.composite_sqlite_file
        self.db = CommsDBTable(self.sqlite_file)
        # grab the ones we need to replace

        self.recs = self.db.select ('*', "WHERE path LIKE '%!%27%' escape '!'")


    def normalize (self):
        for rec in self.recs:
            row = list (rec)
            print row
            path = row[1]
            new_path = path.replace ("%27", "''")
            new_row = copy.copy(row)
            new_row[1] = new_path
            # print '- {}'.format(path)
            # print '    {}'.format(new_path)
            self.db.delete_record("path = '{}'".format (path))
            self.add_record(new_row)


    def add_record (self, row):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        row = list(row)

        # row[1] = globals.normalize_db_path(row[1])
        path = row[1]
        print row

        # quoted_schema = ','.join(map (lambda x:"'%s'" % x, HOSTS_SCHEMA_SPEC))
        quoted_schema = self.db.schema.quoted_schema

        # put data list together to match with schema fields
        quoted_values = ','.join(map (lambda x:u"'{}'".format(x), row))  # current

        if self.dowrites:
            try:
                c.execute("INSERT INTO {tn} ({fn}) VALUES ({fv})" \
                          .format(tn=self.db.table_name, fn=quoted_schema, fv=quoted_values.encode('utf8')))
            except:
                print 'quoted_values is a {}'.format(type(quoted_values))
                print quoted_values
                print('ERROR: {}'.format(sys.exc_info()))
                traceback.print_stack()
                sys.exit()

            conn.commit()
            conn.close()
        else:
            print 'woulda written {}'.format(quoted_values)


if __name__ == '__main__':
    normy = CompositeNormalizer()
    print '{} recs found'.format(len(normy.recs))
    normy.normalize()