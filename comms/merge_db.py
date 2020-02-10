import os, sys, time
import traceback
import globals
import sqlite3
from comms_db import CommsDBTable

"""
create composite table
for each unique table
read in rows,
add to composite
"""

comms_base = '/Users/ostwald/Documents/Comms'

class CompositDB (CommsDBTable):

    def find_dbs (self):
        dbs = []
        for dirname in os.listdir(comms_base):
            db_dir = os.path.join (comms_base, dirname)
            if not os.path.isdir(db_dir):
                continue
            for filename in os.listdir (db_dir):
                if 'composite' not in filename and filename.endswith('.sqlite'):
                    dbs.append(os.path.join (db_dir, filename))
        return dbs

    def add_record (self,row):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        # quoted_schema = ','.join(map (lambda x:"'%s'" % x, HOSTS_SCHEMA_SPEC))
        quoted_schema = self.schema.quoted_schema

        # put data list together to match with schema fields

        escaped_vals = []
        for val in row:
            if type(val) in [type(''), type(u'')]:
                 val = val.replace ("'", "''")
            escaped_vals.append (val)

        quoted_values = ','.join(map (lambda x:u"'{}'".format(x), escaped_vals))  # current

        try:
            c.execute("INSERT INTO {tn} ({fn}) VALUES ({fv})" \
                      .format(tn=self.table_name, fn=quoted_schema, fv=quoted_values.encode('utf8')))
        except:
            print 'quoted_values is a {}'.format(type(quoted_values))
            print quoted_values
            print('ERROR: {}'.format(sys.exc_info()))
            traceback.print_stack()
            sys.exit()

        conn.commit()
        conn.close()

    def ingestDB (self, db_path):
        """
        add all records in specified database
        :param db_path: path that specifies a database file
        :return:
        """
        db = CommsDBTable(db_path)
        rows = db.select_all_records()
        print '{} rows returned'.format(len(rows))
        for row in rows:
            self.add_record (row)
        print 'done ingesting {}'.format(os.path.basename(db_path))

    def ingest_all (self):
        for db_path in self.find_dbs():
            self.ingestDB(db_path)
        print "all dbs ingested!"


if __name__ == '__main__':
    composite_sqlite_File = globals.composite_sqlite_file
    c = CompositDB(composite_sqlite_File)

    # We "merge" various DB's by ingesting them into Composite

    if 0:
        c.ingest_all()

    if 0:
        for name in ['Field Projects', 'VideoEditingDisk1', 'VideoEditingDisk2']:
            path = '/Users/ostwald/Documents/Comms/{}/{}.sqlite'.format(name, name)
            print path
            c.ingestDB (path)

    if 0:
        disk1_path = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk1/CIC-ExternalDisk1.sqlite'
        disk4_path = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk4/CIC-ExternalDisk4.sqlite'
        disk6_path = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk6/CIC-ExternalDisk6.sqlite'
        disk7_path = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk7/CIC-ExternalDisk7.sqlite'

        c.ingestDB (disk7_path)

    if 1:
        stage_path = '/Users/ostwald/Documents/Comms/Staging/Staging.sqlite'
        c.ingestDB(stage_path)