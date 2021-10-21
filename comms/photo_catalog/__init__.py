"""
IN PROGRESS - Create a database from the cvs representation of the FilemakerPro - PhtoCatalogMaster DG

We will store all values as TEXT

"""

import sys, os, re
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
    """
    metadata table stores information about images. Each line may be about a single image or a set of images.
    """
    table_name = 'metadata'

    def __init__(self, sqlite_file, field_list, empty=True):
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

LOC_PAT = re.compile('PC[^[0-9]*([0-9]*)')
class PhotoCatalogRecord:

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        try:
            self.disc_name = self.parse_location()
        except KeyError:
            self.disc_name = 'UNKNOWN'




    def __getitem__ (self, field):
        """
        Provides field-based addressing so that values can be obtained by field name.
        Returns the empty string if the field is not found in the schema
        """
        index = self.parent.schema.index (field)
        # print 'index (%s) : %d' % (field, index)
        if index > -1:
            try:
                ## return self.data[index]
                value = self.data[index]
                if len(value) > 1 and \
                        value[0] == value[-1] == "'" or \
                        value[0] == value[-1] == '"':
                    value = value[1:-1]
                return value
            except:
                return ""
        else:
            return ""

    def get_image_list (self):
        img_num_data = self['Image Numbers']
        img_num_list = []
        for segment in map (lambda x:x.strip(), img_num_data.split(',')):
            if segment in ['SFDD','NFO']:
                # return ['special image_num: {}'.format(segment)]
                # return [segment,]
                img_num_list.append(segment)
                continue
            endpoints = map (int, segment.split('-'))
            # print 'endpoints:', endpoints
            if len(endpoints) == 1:
                img_num_list.append(endpoints[0])
            if len(endpoints) == 2:
                sub_list = range (endpoints[0], endpoints[1]+1)
                img_num_list += sub_list
        return img_num_list

    def get_folder_path (self):
        """
        return a path to this record's folder in de-dp
        """
        location = self.disc_name

        # print 'disc_name', self.disc_name
        base_path = os.path.join (self.parent.DE_DUP_ROOT, self.disc_name)

        return os.path.join (base_path, self['Folder'])

    def parse_location (self):
        location = self['Location']
        if type(location == type('')):
            location = location.strip()
        m = LOC_PAT.match (location)
        if m:
            return 'disc ' + str(m.group(1)).strip()
        else:
            warn_msg = 'Parse WARN: "{}"'.format(self['Location'])
            if 1:
                raise Exception, warn_msg
            else:
                print warn_msg
                return self['Location']

class PhotoCatalogMaster (UserList):
    """
    Read from the data at csv_path and create records in MetadataDB for provided sqlite_file
    """
    schema_spec = None
    # DE_DUP_ROOT = '/Volumes/cic-de-duped/CIC-ExternalDisk1'
    DE_DUP_ROOT = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1'

    def __init__ (self, csv_path, sqlite_file):
        self.data = []
        self.sqlite_file = sqlite_file
        self.db = None
        self.schema = None
        self.bad_records = []
        with open (csv_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            max = None
            i = 0
            for row in reader:
                if len(filter (None, row)) > 0:
                    if self.schema is None:
                        self.schema = row
                    else:
                        # self.data.append(row)
                        try:
                            record = PhotoCatalogRecord(row, self)
                            self.data.append(PhotoCatalogRecord(row, self))
                        except:
                            # print sys.exc_info()[1]
                            self.bad_records.append (row)

                        i = i + 1
                        if max is not None and i >= max:
                            break
        self.db = MetadataDB (self.sqlite_file, self.schema)


    def write_to_db (self):
        for row in self.data:
            try:
                self.db.add_record(row)
            except IOError:
                pass

        print '{} rows written to {}'.format(len(self.data), self.sqlite_file)



def report_rec (rec):
    rec = master.data[rec_num-2]
    print '\nLocation:', rec['Location']
    print 'Folder:', rec.folder
    print 'Image Numbers:',rec['Image Numbers']

    img_list = rec.get_image_list()
    print img_list

    folder_path = rec.get_folder_path()
    print 'folder path:', folder_path
    if not os.path.exists(folder_path):
        print ' -- DOES NOT EXIST'

def folder_path_not_found_report ():
    path = '/Users/ostwald/Documents/Comms/cvs/Weeded_FilemakerPro-PhotoCatalogMaster.csv'
    sqlite_file = '/Users/ostwald/Documents/Comms/cvs/comms_metadata.sqlite'
    # path = '/Users/ostwald/Documents/comms_filemaker/PhotoCatalogMaster-from-Excell.csv'
    # sheet = CsvFile (path)
    master = PhotoCatalogMaster (path, sqlite_file)
    print '{} records read'.format(len(master.data))

    not_found = []
    record_list = master.data[:25]
    for i, rec in enumerate(record_list):
        # report_rec (rec)
        row_num = i + 2

        if i > 0 and i % 100 == 0:
            print '{}/{}'.format(i, len(record_list))

        folder_path = rec.get_folder_path().strip()
        if not os.path.exists(folder_path):
            print '{} - folder not found at "{}"'.format(i, folder_path)
            not_found.append(folder_path)
            if not os.path.exists(normalize_path((folder_path))):
                print '  - normlized path found ...'

    print '\n\n{}/{} of record folder paths could not be found'.format(len(not_found), len(record_list))

    print '{} records could not be read'.format(len(master.bad_records))
    bad_locations = list (set (map (lambda x:x[2], master.bad_records)))
    for r in sorted(bad_locations):
        print '-', r

def normalize_path(path):
    return '/'.join(map (lambda x:x.strip(), path.split ('/')))

if __name__ == '__main__':
    if 0:
        # path = '/Users/ostwald/Documents/Comms/cvs/Weeded_FilemakerPro-PhotoCatalogMaster.csv'
        path = '/Users/ostwald/Downloads/My_Weeded_FilemakerPro-PhotoCatalogMaster.csv'
        sqlite_file = '/Users/ostwald/Documents/Comms/cvs/comms_metadata.sqlite'
        # path = '/Users/ostwald/Documents/comms_filemaker/PhotoCatalogMaster-from-Excell.csv'
        # sheet = CsvFile (path)
        master = PhotoCatalogMaster (path, sqlite_file)
        print '{} records read'.format(len(master.data))

        # master.write_to_db()

    if 0:# lets look at a record
        rec_num = 132
        # sync with googls spreadsheet
        rec = master.data[rec_num-2]

        path = rec.get_folder_path()
        print 'raw', path
        if not os.path.exists (path):
            print 'exists at', path
        else:
            print 'does not exist at', path
        # for ch in path:
        #     print ch, '-', ord(ch)

    if 0:
        loc_pat = re.compile('PC[^[0-9]*([0-9]*)')

        m = loc_pat.match ("PC- 3")
        if m:
            print 'MATCH', m.group(1)
        else:
            print 'no match'

    if 1:
        folder_path_not_found_report ()

