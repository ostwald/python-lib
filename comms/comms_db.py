import sys, os, re, time
from jloFS import JloFile
from UserDict import UserDict
from UserList import UserList
import hashlib

import sqlite3

class Schema_Field:

    def __init__ (self, data):
        self.name = data[0]
        self.type = data[1]
        self.value_fn = data[2]

    def get_value(self, obj):
        if type(self.value_fn) in [type(0), type(''), type (0.5)]:
            return self.value_fn
        else:
            return self.value_fn(obj)

class Schema (UserDict):

    def __init__ (self, spec):
        self.data = {}
        self.fields = UserList()
        self.field_order = UserList()
        for item in spec:
            field = Schema_Field(item)
            self.data[field.name] = field
            self.fields.append(field)
            self.field_order.append(field.name)
        self.quoted_schema = self._get_quoted_schema()

    def get_index (self, field):
        return self.field_order.index(field)

    def _get_quoted_schema(self):
        return ','.join(map (lambda x:"'%s'" % x, self.field_order))

    def obj_to_data_values(self, obj):
        row_value_list = []
        for field in self.fields:
            val = field.get_value(obj)
            if type(val) == type(''):
                row_value_list.append("'{}'".format(val.replace ("'", "%27")))
            if type(val) == type(1) or type(val) == type(1.5):
                row_value_list.append(str(val))
        quoted_values = ','.join(row_value_list)

        return quoted_values

def get_time_str(secs):
    date_time_fmt = '%Y-%m-%d %H:%M:%S'
    return time.strftime(date_time_fmt, time.localtime(secs))

def get_checksum(path):
    m = hashlib.new('md5')
    m.update (open (path, 'r').read())
    return m.hexdigest()

class CommsDBTable:

    table_name = 'comms_files'
    schema_spec = [
        ['file_name', 'TEXT', lambda x:x.name],
        ['path', 'TEXT', lambda x:x.path],
        ['extension', 'TEXT', lambda x:x.ext],
        ['image_type', 'TEXT', ''],  # jpg and JPG are both JPEG, cr2 and crw are both RAW
        ['size', 'INTEGER', lambda x:x.size],
        ['check_sum', 'TEXT', lambda x:get_checksum(x.path)],
        # ['date_created', 'FLOAT', lambda x:x.ctime],
        ['date_created', 'TEXT', lambda x:get_time_str(x.ctime)],
        # ['date_modified', 'FLOAT', lambda x:x.modtime],
        ['date_modified', 'TEXT', lambda x:get_time_str(x.modtime)],
        ['notes', 'TEXT', ''],
    ]

    def __init__(self, sqlite_file):
        self.sqlite_file = sqlite_file
        self.schema = Schema(self.schema_spec)
        if not self.table_exists():
            self.db_setup()

    def table_exists (self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}';" \
                  .format(tn=self.table_name))
        tables = c.fetchall()
        conn.close()
        return len(tables)

    def db_setup(self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        # apparently we need at least one field to create a record
        first_field = self.schema.fields[0]
        c.execute('CREATE TABLE {tn} ({fn} {ft})' \
                  .format(tn=self.table_name, fn=first_field.name, ft=first_field.type))

        if len(self.schema.fields)  > 1:
            for field in self.schema.fields[1:]:
                c.execute("ALTER TABLE {tn}  ADD COLUMN '{cn}' {ct}" \
                          .format(tn=self.table_name, cn=field.name, ct=field.type))

        conn.commit()
        conn.close()

    def add_record (self,file_obj):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        # quoted_schema = ','.join(map (lambda x:"'%s'" % x, HOSTS_SCHEMA_SPEC))
        quoted_schema = self.schema.quoted_schema

        # put data list together to match with schema fields
        quoted_values = self.schema.obj_to_data_values(file_obj)
        # print quoted_values

        try:
            c.execute("INSERT INTO {tn} ({fn}) VALUES ({fv})" \
                      .format(tn=self.table_name, fn=quoted_schema, fv=quoted_values))
        except:
            print('ERROR: {}'.format(sys.exc_info()))

        conn.commit()
        conn.close()

    def delete_record (self, where_condition):
        """
        DELETE FROM table_name WHERE condition;
        """
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        query = "DELETE from {} WHERE {}".format(self.table_name, where_condition)

        # print query

        c.execute(query)
        # print 'records affected: {}'.format(conn.total_changes)
        conn.commit()

    def select_all_records (self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        query = "SELECT * from {}".format(self.table_name)

        c.execute(query)
        rows = c.fetchall()
        # return map(lambda x:x[0], rows)
        return rows

    def select (self, fields, where_clause=None):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        if where_clause is None:
            where_clause = ''
        query = "SELECT {} FROM {} {}".format(fields, self.table_name, where_clause)

        # print query

        c.execute(query)
        rows = c.fetchall()
        return rows

def show_file(path):
    obj = JloFile (path)
    print 'name: {} ({})'.format(obj.name, type(obj.name))
    print 'created: {} ({})'.format(time.ctime(obj.ctime), type(obj.ctime))
    print 'modified: {} ({})'.format(time.ctime(obj.modtime), type(obj.modtime))
    print 'size: {} ({})'.format(obj.size, type(obj.size))
    print 'ext: {} ({})'.format(obj.ext, type(obj.ext))

if __name__ == '__main__':

    sqlite_file = '/Users/ostwald/tmp/comms_db.sqlite'

    if 0:
        if not table_exists(table_name):
            db_setup()

        # add_date ("2018-10-31")
        # add_date ("2018-10-26")
        # add_date ("2018-10-01")
        # add_date ("2018-10")
        add_date ("10/28/2018")

    if 0:
        path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk2/staff.jpg'
        show_file(path)

    if 1:
        table = CommsDBTable(sqlite_file)
        path = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk2/staff.jpg'
        obj = JloFile(path)
        print table.add_record(obj)