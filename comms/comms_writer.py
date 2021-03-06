import os, sys, shutil, traceback
from comms_db import CommsDBTable
import globals
import sqlite3

class DBRecord:

    def __init__ (self, row_data):
        self.data = row_data
        self.path = row_data[1]
        self.size = row_data[4]
        self.filename = row_data[0]
        self.checksum = row_data[5]
        self.root, self.ext = os.path.splitext(self.filename)

class Writer:
    """
    writes files to disk
    - only if they do not exist at that path
    write records to a dest_sqlite_file
    - existing dest_sqlite_file deleted at __init__
    """

    src_base_dir = '/Volumes/archives/CommunicationsImageCollection'
    dest_base_dir = '/Volumes/cic-de-duped'
    start_with_frest_dest_sqlite_file = False
    dowrites = 1

    def __init__ (self, src_sqlite_file, dest_sqlite_file, path_pat=None):
        """

        :param src_sqlite_file: database file from which records are selected
        :param dest_sqlite_file: the database to which records are added
        :param path_pat: used to select the records that will be written
        """
        self.src_sqlite_file = src_sqlite_file
        self.dest_sqlite_file = dest_sqlite_file

        if self.start_with_frest_dest_sqlite_file:
            if os.path.exists(self.dest_sqlite_file):
                print 'deleting exsting db file at: {}'.format(self.dest_sqlite_file)
                os.remove(self.dest_sqlite_file)

        self.src_db = CommsDBTable(self.src_sqlite_file)
        self.dest_db = CommsDBTable(self.dest_sqlite_file)

        # self.records = map (DBRecord, self.src_db.select_all_records())
        # self.records = self.src_db.select_all_records(sort_spec='path ASC')
        self.records = self.get_records_to_write(path_pat)
        print 'there are {} records'.format(len(self.records))

    def get_records_to_write (self, path_pat=None):
        # print 'get_records_to_write: "{}"'.format(path_pat)
        if path_pat is None:
            return self.src_db.select_all_records(sort_spec='path ASC')
        else:
            return self.src_db.select('*', "WHERE path LIKE '%{}%'".format(path_pat))

    def get_dest_path (self, src_path):
        dest_rel_path = src_path.replace(self.src_base_dir, '')
        if dest_rel_path.startswith('/Staging'):
            dest_rel_path = dest_rel_path.replace ('/Staging', '/Field Projects')
        # dest_path = src_path.replace (self.src_base_dir, self.dest_base_dir)
        dest_path = self.dest_base_dir + dest_rel_path
        return dest_path

    def write_all_records (self, start=0):
        num_recs = len(self.records)

        i = start
        for rec in self.records[start:]:
            self.write_record(rec)
            i += 1
            if i > 0 and i % 100 == 0:
                print u'{}/{}'.format(i, num_recs)

    def write_record (self, rec):
        """

        :param rec: a db_record
        :return:
        """
        rec = list(rec)  # to clone row of data
        src_path = rec[1] # path is the second field
        dest_path = self.get_dest_path(src_path)

        # escape quote for sql
        rec[1] = dest_path.replace ("'", "''")
        if not self.db_rec_exists(rec[1]):
            self.add_dest_record(rec)

        dest_file_path = globals.normalize_file_path(dest_path)
        src_file_path = globals.normalize_file_path(src_path)
        if self.dowrites:
            if not os.path.exists(os.path.dirname(dest_file_path)):
                os.makedirs(os.path.dirname(dest_file_path))
            if not os.path.exists(dest_file_path):
                shutil.copy2 (src_file_path, dest_file_path)
        else:
            if not os.path.exists(dest_file_path):
                print ' - would have copied from ', src_file_path
        print u' - {} ({})'.format(dest_file_path, rec[4])

    def db_rec_exists (self, path):
        """
        return True if this path exists in the Destination DB
        """
        try:
            normalized = globals.normalize_db_path(path)
            # print 'normalized: {}'.format(normalized)
            return self.dest_db.count_selected("WHERE path = '{}'".format(normalized))
        except:
            print u'ERROR: db_rec_exists choked on "{}"'.format(normalized)
            return False

    def add_dest_record (self,row):

        conn = sqlite3.connect(self.dest_sqlite_file)
        c = conn.cursor()

        # quoted_schema = ','.join(map (lambda x:"'%s'" % x, HOSTS_SCHEMA_SPEC))
        quoted_schema = self.dest_db.schema.quoted_schema

        # put data list together to match with schema fields
        quoted_values = ','.join(map (lambda x:u"'{}'".format(str (x).replace("'", "''")), row))  # current

        try:
            c.execute("INSERT INTO {tn} ({fn}) VALUES ({fv})" \
                      .format(tn=self.dest_db.table_name, fn=quoted_schema, fv=quoted_values.encode('utf8')))
        except:
            print 'quoted_values is a {}'.format(type(quoted_values))
            print quoted_values
            print('ERROR: {}'.format(sys.exc_info()))
            traceback.print_stack()
            sys.exit()

        conn.commit()
        conn.close()

if __name__ == '__main__':

    sqlite_file = globals.composite_sqlite_file
    dest_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'

    path_pat = 'Field Project-PREDICT-FP17 (2011)/Disc 8/'
    # path_pat = None
    writer = Writer(globals.composite_sqlite_file, dest_sqlite_file, path_pat)
    start = 0
    writer.write_all_records(start=start)


