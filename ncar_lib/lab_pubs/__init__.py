"""
citation data for pubs is downloaded from WOS (assumably using NCAR authors).

The resulting database has lots of data about each pub, including DOI

NCAR Lib wants this data only for records from a certain lab in a certain time span,
and only for pubs that have primary author from particular lab.

in the first step, I used admin-utils/ncarlibadmin/report/lab_reporter.py to create a CSV
of doi to pid for ONLY THE PUBS that NCAR Lib wants.

Next, we have to
1 - read the citation data spreadsheet
2 - Select only the pubs with DOIs that are mapped to pids
3 - Insert pids in records
4 - write selected records (containing pids) to new CSV

"""
import os, sys, re
from tabdelimited import CsvFile, CsvRecord

def get_doi_pid_map ():

    pid_doi_path = '/Users/ostwald/tmp/RAL_pubs.csv'
    csv = CsvFile ()
    csv.read(pid_doi_path)
    print '{} records read'.format(len(csv.data))
    doi_map = {}
    for rec in csv:
        if rec['doi'] is None or rec['doi'].strip() == '':
            # print '{} has no doi'.format(rec['pid'])
            pass
        else:
            doi_map[rec['doi']] = rec['pid']
    return doi_map

class RawCsv(CsvFile):

    def __init__ (self):
        CsvFile.__init__ (self)
        self.read ('/Users/ostwald/Downloads/08012018_publication_data_raw.csv')
        print 'raw file contains {} records'.format(len (self.data))

    def get_doi_map (self):
        doi_map = {}
        for rec in self.data:
            if rec['DOI'] is None or rec['DOI'].strip() == '':
                continue
            doi_map[rec['DOI']] = rec
        return doi_map

    def make_pid_csv (self):
        lines = [];add=lines.append
        header = list(rc.schema.data)   # make a clone
        header.insert (0, 'PID')
        add (header)

        doi_pid_map = get_doi_pid_map()
        doi_rec_map = self.get_doi_map()

        pid_map_keys = doi_pid_map.keys()
        for doi in pid_map_keys:
            if not doi_rec_map.has_key(doi):
                # print 'doi_rec_map does not have {}'.format(doi)
                print '{} - {}'.format(doi_pid_map[doi], doi)
                continue
            data = list(doi_rec_map[doi].data)  # make a clone
            data.insert(0, doi_pid_map[doi])
            add (data)

        return '\n'.join (map (lambda x:'\t'.join(x), lines))

if __name__ == '__main__':

    # print dm['10.1029/2017EO088041']

    rc = RawCsv()

    if 0:
        doi_pid_map = get_doi_pid_map()
        doi_rec_map = rc.get_doi_map()

        doi = '10.1002/2013JD021227'

        if doi_pid_map.has_key(doi):
            print 'doi_pid_map has key {}'.format(doi)

        if doi_rec_map.has_key(doi):
            print 'doi_rec_map has key {}'.format(doi)

    else:
        tabdelimited = rc.make_pid_csv()
        path = '/Users/ostwald/tmp/NEW_PUBS.txt'
        fp = open (path, 'w')
        fp.write (tabdelimited)
        fp.close()
        print 'wrote to {}'.format(path)

