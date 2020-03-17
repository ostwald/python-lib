"""
IN PROGREDS - Create a database from the cvs representation of the FilemakerPro - PhtoCatalogMaster DG

We will store all values as TEXT

"""

import sys, os
from UserList import UserList
from UserDict import UserDict
from comms.comms_db import CommsDBTable, Schema, Schema_Field
import sqlite3
import csv


class MD_Schema_Field (Schema_Field):

    def __init__ (self, data):
        self.name = data[0]
        self.type = data[1]

class MD_Schema (UserDict):

    def __init__ (self, spec):
        self.data = {}
        self.fields = UserList()
        self.field_order = UserList()
        for item in spec:
            field = MD_Schema_Field(item)
            self.data[field.name] = field
            self.fields.append(field)
            self.field_order.append(field.name)
        self.quoted_schema = self._get_quoted_schema()

    def get_index (self, field):
        return self.field_order.index(field.name)

    def _get_quoted_schema(self):
        return ','.join(map (lambda x:"'%s'" % x, self.field_order))

    def obj_to_data_values(self, obj):
        row_value_list = []
        for field in self.fields:
            val = obj[self.get_index(field)]
            if type(val) == type(''):
                # row_value_list.append("'{}'".format(val.replace ("'", "%27")))
                row_value_list.append("'{}'".format(val.replace("'", "\'\'")))
            if type(val) == type(1) or type(val) == type(1.5):
                row_value_list.append(str(val))
        # quoted_values = ','.join(map (lambda x:x.replace ("'", "''"), row_value_list))
        quoted_values = ','.join(row_value_list)

        return quoted_values

class MetadataDB (CommsDBTable):
    table_name = 'metadata'

    def __init__(self, sqlite_file, field_list):
        self.sqlite_file = sqlite_file

        # start out blank
        if os.path.exists(self.sqlite_file):
            os.remove (self.sqlite_file)

        # self.schema = Schema(self.schema_spec)
        self.schema = self.make_schema(field_list)
        if not self.table_exists():
            self.db_setup()


    def make_schema (self, field_list):
        schema_spec = []
        for field in field_list:
            schema_spec.append ([field, 'TEXT'])
        return MD_Schema (schema_spec)



class PhotoCatalogMaster (UserList):
    """
    Read from the data at csv_path and create records in DB for provided sqlite_file
    """
    schema_spec = None

    def __init__ (self, csv_path, sqlite_file):
        self.data = []
        self.sqlite_file = sqlite_file
        self.db = None
        self.schema = None
        with open (csv_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if self.schema is None:
                    self.schema = row
                else:
                    self.data.append(row)

        self.db = MetadataDB (self.sqlite_file, self.schema)


    def write_to_db (self):
        for row in self.data:
            try:
                self.db.add_record(row)
            except IOError:
                pass

        print '{} rows written to {}'.format(len(self.data), self.sqlite_file)



if __name__ == '__main__':
    path = '/Users/ostwald/Documents/comms_filemaker/FilemakerPro-PhotoCatalogMaster.csv'
    sqlite_file = '/Users/ostwald/Documents/comms_filemaker/comms_metadata.sqlite'
    # path = '/Users/ostwald/Documents/comms_filemaker/PhotoCatalogMaster-from-Excell.csv'
    # sheet = CsvFile (path)
    master = PhotoCatalogMaster (path, sqlite_file)
    print '{} records read'.format(len(master.data))

    master.write_to_db()
