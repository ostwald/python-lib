"""
a reader for the files created by DupReporter (in dup_finder_reporter)

these files consist of dup sets like this:

CIC-ExternalDisk1/photos/1-archived/FP 22 DC3/disc6/_MG_2209.CR2 *
 - Field Projects/Field Project-DC3-FP19/Disc 4/_MG_2209.CR2
 - Field Projects/Field Project-DC3-FP22/Disc 6/_MG_2209.CR2

 the files are created for each directory, and are stored in the same hierarchical
 structure as the directories they represent (only the files had a .txt suffix)
"""
import sys, os, traceback, re
from UserList import UserList

class DupSet:
    def __init__ (self, file_dup, other_dups):
        self.file = file_dup
        self.duplist = [self.file]
        for path in filter (None, map (lambda x:x.strip(), other_dups.split('\n'))):
            self.duplist.append(path)


class DupReportReader:

    dupset_pat = re.compile('\\n(CIC-ExternalDisk1.*)')

    def __init__ (self, path):
        self.path = path
        self.root_dir = None
        self.data = []
        self.read()

    def read(self):

        s = open(self.path, 'r').read()
        splits = self.dupset_pat.split(s)
        # print len(splits), 'splits'

        for i, s in enumerate(splits):
            if i == 0:
                continue
            if s.startswith('CIC-ExternalDisk1'):
                file_dup = s
            else:
                self.data.append (DupSet(file_dup, s))

def count_dups (path):
    if os.path.isfile(path):
        reader = DupReportReader(path)
        count = len(reader.data)
        print path, '--' , count
    if os.path.isdir(path):
        count = 0
        for filename in os.listdir(path):
            if filename[0] == '.':
                continue
            count += count_dups (os.path.join (path, filename))
    return count

def gather_dup_sets(path):
    if os.path.isfile(path):
        reader = DupReportReader(path)
        dupsets = reader.data
    if os.path.isdir(path):
        dupsets = []
        for filename in os.listdir(path):
            if filename[0] == '.':
                continue
            dupsets += gather_dup_sets (os.path.join (path, filename))
    return dupsets

if __name__ == '__main__':
    if 0:
        path = '/Users/ostwald/Documents/Comms/dup_reports/ExternalDisk1/photos/1-archived/FP 22 DC3/disc6.txt'
        reader = DupReportReader(path)
        print len(reader.data), 'read'

    if 0:
        path = '/Users/ostwald/Documents/Comms/dup_reports/ExternalDisk1/photos/1-archived/'
        count = count_dups(path)
        print 'count is', count

    if 1:
        path = '/Users/ostwald/Documents/Comms/dup_reports/ExternalDisk1/photos/1-archived/'
        dupsets = gather_dup_sets(path)
        print len(dupsets), 'dupsets'

        def has_fp_dup (dupset):
            return 'Field Projects/' in ' '.join(dupset.duplist)

        # fp_dupsets = filter (lambda x:has_fp_dup(x), dupsets)
        fp_dupsets = filter (has_fp_dup, dupsets)
        print len(fp_dupsets), 'fp_dupsets'

    if 0:
        pat = re.compile('\\n(CIC-ExternalDisk1.*)')
        foo = '\nCIC-ExternalDisk1/photos/1-archived/FP 22 DC3/disc6/_MG_2211.CR2 *\n- Field Projects/Field Project-DC3-FP19/Disc 4/_MG_2211.CR2'
        m = pat.match(foo)
        if m:
            print m.group(1)