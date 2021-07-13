"""
Tools to create CSV files for ingesting into Omeka
"""
import os, sys, traceback
from UserDict import UserDict
from comms import CommsDBTable, DupManager, get_checksum

SCHEMA = [
    'Dublin Core:Title',
    'Dublin Core:Description',
    'Dublin Core:Creator',
    'Dublin Core:Publisher',
    'Dublin Core:Date',
    'Dublin Core:Contributor',
    'Dublin Core:Rights',
    'Dublin Core:Format',
    'Dublin Core:Type',
    'Dublin Core:Identifier',
    'Dublin Core:Coverage',
    'Files',
    'Tags'
]

class DBRecord:

    def __init__ (self, data, schema_spec):
        self.data = data
        self.schema = map (lambda x:x[0], schema_spec)

    def __getitem__ (self, field):
        index = self.schema.index(field)
        return self.data[index]

class OmekaRecord (UserDict):

    """
    given a de-dup path
    - get the dedup record
        - if path can't be found
        - then compute and use checksum
    - get dup paths
    - get spreadsheet row
    """

    dc_fields = {
        'Title': None, # 'image file name',
        'Description':  None, # 'from spreadsheet',
        'Creator': 'Carlye Calvin',
        'Publisher': 'University Corporation for Atmospheric Research',
        'Date':  None, # 'from spreadsheet',
        'Contributor': 'UCAR Communications',
        'Rights': 'Copyright University Corporation for Atmospheric Research (UCAR). This work is licensed under a Creative Commo\
ns Attribution-NonCommercial 4.0 International License.',
        'Format':  None, # 'image file suffix',
        'Type': 'Still Image',
        'Identifier':  None, # '???? (checksum?)',
        'Coverage':  None, # 'location edited by hand',
    }

    # sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    # dup_data_path = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'

    # def __init__ (self, img_path, catalog_data, url_base):
    def __init__ (self, img_path, writer, eponymous=0):
        print img_path

        self.img_path = img_path
        self.writer = writer
        self.db = self.writer.db_table
        self.dup_manager = self.writer.dup_manager
        try:
            self.db_record = self.get_db_record()
        except:
            pass


        self.catalog_data = self.writer.catalog_record
        self.url_base = self.writer.image_url_base
        self.data = {}
        self.data.update (self.dc_fields)
        self.identifier = self.make_id()
        if eponymous:
            self.description = self.get_eponymous_description()
        else:
            self.description = self.catalog_data['Note']

        self.data.update ({
            'Title' : os.path.basename(img_path),
            'Date' : self.catalog_data['Date Original'],
            'Description' : self.description,
            'Tags' : self.catalog_data['Keywords'],
            'Files' : self.make_url(),
            'Format': os.path.basename(self.img_path).split('.')[-1].lower(),
            'Identifier': self.make_id(),
        })

    def make_id (self):
        segments = [
            self.catalog_data['Location'],
            self.catalog_data['Folder'],
            os.path.basename(self.img_path)
        ]
        return '_'.join(segments)

    def make_url (self):
        return os.path.join (self.url_base, os.path.basename(self.img_path))

    def get_db_record (self):

        recs = self.db.select('*', "WHERE path='{}'".format(self.img_path))
        if len(recs) < 1:
            checksum = get_checksum(self.img_path)
            print 'checksum:', checksum
            recs = self.db.select ('*', "WHERE check_sum = '{}'".format(checksum))
        if len(recs) < 1:
            raise KeyError, 'record not found for {}'.format(self.img_path)
        else:
            return DBRecord(recs[0], self.db.schema_spec)

    def get_eponymous_description (self):
        root = os.path.splitext (os.path.basename(self.img_path))[0]
        splits = map (lambda x:x.title(), root.split('-'))
        return ' '.join(splits)

    def as_tab_delimited (self):
        data = []
        for field in SCHEMA:
            field = field.replace ('Dublin Core:', '')
            val = self[field]
            if val is None:
                val = ''
            data.append(val)
        return '\t'.join(data)

    def __repr__ (self):
        s = ''
        for key in self.keys():
            s += ' - {}: {}\n'.format(key, self[key])
        return s

class TSVWriter:

    # sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'
    dup_data_path = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'

    def __init__ (self, image_dir, catalog_record, image_url_base):
        self.image_dir = image_dir
        self.catalog_record = catalog_record
        self.image_url_base = image_url_base
        self.db_table = CommsDBTable (self.sqlite_file)
        self.dup_manager = DupManager(self.dup_data_path)

    def accept_file (self, filename):
        root, ext = os.path.splitext(filename)
        if ext.lower() not in ['.jpg', '.jpeg', '.tif', '.tiff', '.cr2']:
            return 0
        return 1

    def process (self):
        max = 111
        lines = []
        lines.append ('\t'.join(SCHEMA))
        for i, filename in enumerate(os.listdir(self.image_dir)):
            if not self.accept_file(filename):
                continue
            img_path = os.path.join(self.image_dir, filename)

            # rec = OmekaRecord(img_path, self.catalog_record, self.image_url_base)
            try:
                rec = OmekaRecord(img_path, self, 1)
            except:
                # print traceback.print_exc()
                print 'ERROR - could not process {}'.format(os.path.basename(img_path))
                continue
            # print rec

            try:
                checksum = rec.db_record['check_sum']
                dup_paths = get_dup_paths(checksum)
            except:
                dup_paths = [img_path]

            print filename, len(dup_paths), 'dup paths'

            lines.append(rec.as_tab_delimited())
            if i + 1 >= max:
                break

        outpath = "/Users/ostwald/tmp/OMEKA_INgeST_{}.tsv".format(os.path.basename(self.image_dir))
        fp = open (outpath,'w')
        fp.write ('\n'.join(lines) + '\n')
        fp.close()
        print 'wrote to', outpath

    def get_dup_paths(self, checksum):

        try:
            return self.dup_manager.find_dups_for_checksum(checksum)
        except:
            raise Exception, 'no dups found for {}'.format(checksum)


def import_mosquito_images():
    # Set 2 - MOSQUITOES

    # - (the jpegs have been removed in de-duped but they are available in the main CIC collection)
    # /Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 224/mosquito research part 2/mosquitoes

    # from Catalog spreadsheet row - see Weeded_FilemakerPro-PhotoCatalogMaster_JLO_2021-01-07
    photo_catalog_master_data = {
        'Date Original' : '7/19/2016',
        'Location' : 'PC-224',
        'Folder' : 'mosquito research part 2/mosquitoes',
        'Note' : 'mosquito research Sara Paull, Mary Hayden, and Savannah Mullis collecting mosquito samples near Ft. Collins, Colorado',
        'Keywords' : 'Scientist',
    }
    img_dir = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 224/mosquito research part 2/mosquitoes'

    url_base = "https://osws.ucar.edu/comms/mosquitoes"

    writer = TSVWriter(img_dir, photo_catalog_master_data, url_base)
    writer.process()

def import_beachon_2010_images():
    # CASE 1 - BEACHON_2010

    # from Catalog spreadsheet row - see Weeded_FilemakerPro-PhotoCatalogMaster_JLO_2021-01-07
    photo_catalog_master_data = {
        'Date Original' : '8/13/2010',
        'Location' : 'PC-221',
        'Folder' : 'BEACHON_2010',
        'Note' : 'Aftermath of the Haymen Fire of 2002, 35 miles northwest of Colorado Springs, CO ' + \
                 'BEACHON field project, Peter Harley, Manitou Experimental Forest ' + \
                 'Tower with instrumentation used in the BEACHON field project in Manitou Springs, CO ',
        'Keywords' : 'Field Projects',
    }
    img_dir = '/Volumes/cic-de-duped/CIC-ExternalDisk1/disc 221/BEACHON_2010'

    url_base = "https://osws.ucar.edu/comms/BEACHON_2010"

    writer = TSVWriter(img_dir, photo_catalog_master_data, url_base)
    writer.process()

if __name__ == '__main__':
    # CASE 3 - scientists

    # from Catalog spreadsheet row - see Weeded_FilemakerPro-PhotoCatalogMaster_JLO_2021-01-07
    photo_catalog_master_data = {
        'Date Original' : '4/4/2018',
        'Location' : 'PC-227',
        'Folder' : 'scientists-jpgs',
        'Note' : '',
        'Keywords' : 'StaffScientist',
    }
    img_dir = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/disc 227/scientists-jpgs'

    url_base = "https://osws.ucar.edu/comms/scientists"

    writer = TSVWriter(img_dir, photo_catalog_master_data, url_base)
    writer.process()