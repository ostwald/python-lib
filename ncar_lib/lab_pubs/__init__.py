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
from UserList import UserList
from tabdelimited import CsvFile, CsvRecord, FieldList
import csv


def get_pid_list (path):
    """
    extract pids from a file created by ncarlibadmin/report/lab_pub_reporter.py
    :return:
    """

    csv = CsvFile ()
    csv.read(path)
    print '{} records read'.format(len(csv.data))
    pid_list = map (lambda x:x['pid'], csv.data)
    return pid_list

class MyCsvReader (UserList):

    def __init__ (self, affiliation):
        self.affiliation = affiliation
        self.report_path = '/Users/ostwald/downloads/{}anyauthor 20140101topresent.csv'.format(self.affiliation)
        self.data = []
        self.schema = None
        with open(self.report_path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if self.schema is None:
                    self.schema = self.makeSchema(row)
                else:
                    self.data.append(CsvRecord (row, self))

        self.filter_pid_list = get_pid_list('/Users/ostwald/tmp/{}_pubs.csv'.format(self.affiliation))

    def makeSchema (self, data):
		"""
		override for CVS, etc
		"""
		# print 'schema line: ', data
		return FieldList(data)

    def get_pid_map (self):
        pid_map = {}
        for rec in self.data:
            if rec['pid'] is None or rec['pid'].strip() == '':
                continue
            pid_map[rec['pid']] = rec
        return pid_map

    def filter_by_pid_list (self):
        lines = [];add=lines.append
        header = list(self.schema.data)   # make a clone
        add (header)
        pid_map = self.get_pid_map()
        for pid in  self.filter_pid_list:
            rec = pid_map[pid]
            add (rec.data)

        return '\n'.join (map (lambda x:'\t'.join(x), lines))

    def write_filtered (self, path=None):
        if path is None:
            path = '/Users/ostwald/tmp/{}_first_authors.txt'.format(self.affiliation)
        fp = open (path, 'w')
        fp.write (self.filter_by_pid_list())
        fp.close()
        print 'wrote to {}'.format(path)

if __name__ == '__main__':

    affiliation = 'MMM'
    # pid_data = '/Users/ostwald/tmp/{}_pubs.csv'.format(affiliation)
    # pid_list = get_pid_list(pid_data)
    # print '{} pids read'.format(len(pid_list))

    # rc = RawCsv()

    if 1:
        report_path = '/Users/ostwald/downloads/{}anyauthor 20140101topresent.csv'.format(affiliation)
        reader = MyCsvReader(affiliation)
        print '{} records read'.format(len(reader.data))
        # pid_map = reader.get_pid_map()
        # print '{} pids in map'.format(len(pid_map))

        # keys = pid_map.keys()
        # for pid in pid_list:
        #     if not pid in keys:
        #         print '{} not in keys'.format(pid)
        #     else:
        #         print '{}'.format(pid)



        # filtered = reader.make_pid_csv(pid_list)
        # print 'filtered has {} records'.format(len(filtered))
        # print 'filtered is a {}'.format(type(filtered))
        # print filtered

        reader.write_filtered()

    elif 0:
        tabdelimited = rc.make_pid_csv()
        path = '/Users/ostwald/tmp/NEW_PUBS.txt'
        fp = open (path, 'w')
        fp.write (tabdelimited)
        fp.close()
        print 'wrote to {}'.format(path)

