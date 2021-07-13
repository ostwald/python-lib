"""
sometimes we aggregated dups in the wrong place.
and later we want to "shift" them to another place.

e.g., consider this dupset:

Field Projects/Field Project-DC3-FP19/Disc 7/_MG_1698.CR2
 - CIC-ExternalDisk1/photos/1-archived/FP 22 DC3/disc3/_MG_1698.CR2 *
 - Field Projects/Field Project-DC3-FP22/Disc 3/_MG_1698.CR2

We would rather the file for this dupset be within a Field Project, and
not within CIC-ExternalDisk1/photos

dup_shifter is a DupManager that moves the dups to a desired location and
updates the databased accordingly
"""
import os, sys
from dup_manager import DupManager, DupSet
from comms.utils import DupFinder
from comms_db import CommsDBTable
from UserDict import UserDict

class AlreadyProcessedException (Exception):
    pass

class ArchiveDstDoesNotExist (Exception):
    pass

class TallyDict(UserDict):
    """
    the buckets are lists

    use the "add" method to add an item to a bucket's list
    """

    def __getitem__(self, key):
        if not self.data.has_key(key):
            return []
        else:
            return self.data[key]

    def add(self, key, val):
        vals = self[key]
        vals.append(val)
        self.data[key] = vals

    def keys(self):
        return sorted(self.data.keys())


class DupShifter(DupFinder):
    composite_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'
    dedupe_sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
    cache_path = '/Users/ostwald/tmp/DUPSETS_TO_SHIFT.txt'

    def __init__(self, dup_data_path):
        DupFinder.__init__(self, dup_data_path)
        self.composite_DB = CommsDBTable(self.composite_sqlite_file)
        self.dedupe_DB = CommsDBTable(self.dedupe_sqlite_file)

    def get_path_for_checksum(self, checksum, db):
        """
        find the path in the given database for the given checksum
        :param checksum:
        :param db:
        :return:
        """
        try:
            recs = db.select('path', "WHERE check_sum = '{}'".format(checksum))
            if len(recs) == 0:
                raise Exception("record not found in {} for {}".format(
                    os.path.basename(db.sqlite_file), checksum))
            if len(recs) > 1:
                raise Exception("{} records found in {} for {}".format(
                    len(recs), os.path.basename(db.sqlite_file), checksum))
            return recs[0][0]
        except Exception, msg:
            raise 'could not get database record: {}'.format(msg)

    def get_checksum_for_path(self, path, db):
        try:
            recs = db.select('check_sum', "WHERE path = '{}'".format(path))
            if len(recs) == 0:
                raise Exception("record not found in {} for {}".format(
                    os.path.basename(db.sqlite_file), path))
            if len(recs) > 1:
                raise Exception("{} records found in {} for {}".format(
                    len(recs), os.path.basename(db.sqlite_file), path))
            return recs[0][0]
        except Exception, msg:
            raise 'could not get database record: {}'.format(msg)

    def get_cached_dupsets_to_shift(self):
        return map(lambda x: x.strip(), filter(None, open(self.cache_path, 'r').read().split('\n')))

    def get_dupsets_containing(self, *substrings):
        dupsets = []
        for key in self.dup_map.keys():
            dups = self.dup_map[key]
            blob = ' '.join(dups)
            # all substrings must be found
            found = True
            for s in substrings:
                if not s in blob:
                    found = False
                    break
            if found:
                dupsets.append(key)
        # print len(dupsets), 'dupsets found'
        return dupsets

    def cache_dupsets_to_shift(self):
        """
        we want to shift files within CIC-ExternalDisk1/photos that
        have dups in a Field Project
        :return:
        """
        pat_1 = 'CIC-ExternalDisk1/photos/'
        pat_2 = 'Field Projects/'
        pat_2 = 'Staging/'

        # get dupsets containing pat_1 and pat_2
        dupsets = self.get_dupsets_containing(pat_1, pat_2)

        dupsets_to_shift = []
        for i, key in enumerate(dupsets):
            paths = list(set(map(self.make_deduped_path, self.dup_map[key])))
            paths.sort()
            if i > 0 and i % 100 == 0:
                print '{}/{}'.format(i, len(dupsets))
            for path in paths:
                exists = os.path.exists(path) and '*' or ''
                # print '-', path, exists

                if exists == '*' and pat_1 in path:
                    dupsets_to_shift.append(key)
                    break
        print len(dupsets_to_shift), 'dupsets_to_shift'

        fp = open(self.cache_path, 'w')
        fp.write('\n'.join(dupsets_to_shift))
        fp.close()
        print 'wrote to', self.cache_path

        return dupsets_to_shift

    def report_field_project_dupsets_containing_photos(self):
        base_dir = '/Volumes/cic-de-duped/Field Projects'
        pat_1 = 'CIC-ExternalDisk1/photos/'
        total = 0
        for filename in os.listdir(base_dir):
            if filename[0] == '.':
                continue
            pat_2 = "Staging/{}".format(filename)
            dupsets = self.get_dupsets_containing(pat_1, pat_2)
            print filename, ' - ', len(dupsets)
            total += len(dupsets)
        print 'total:', total

    def report_cached_dupsets(self):
        """
        create a tally showing the dupsets within each of the top-level directories
        of "Field Projects"
        :return:
        """
        tally = TallyDict()
        keys = self.get_cached_dupsets_to_shift()
        staging_mask = '/Volumes/archives/CommunicationsImageCollection/Staging'
        staging_mask_splits = staging_mask.split('/')
        for checksum in keys:
            # print '\n', checksum
            duplist = self.find_dups_for_checksum(checksum)
            duplist.sort
            dest = None
            for path in duplist:
                # print path
                if staging_mask in path:
                    bucket = path.split('/')[len(staging_mask_splits)]
                    # print 'bucket:', bucket
                    tally.add(bucket, path)

        print '\nTally'
        for key in tally.keys():
            print "- {} - {}".format(key, len(tally[key]))

    def get_shift_map(self, bucket_list=None):
        """
        create a tally showing the source and destination of all the shifts that will
        happen  within each of the top-level directories
        of "Field Projects"
        :return:
        """
        shift_map = TallyDict()
        keys = self.get_cached_dupsets_to_shift()
        # staging_mask = '/Volumes/archives/CommunicationsImageCollection/Staging'
        # photos_mask = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/photos'

        staging_mask = '/Volumes/cic-de-duped/Field Projects'
        photos_mask = '/Volumes/cic-de-duped/CIC-ExternalDisk1/photos'

        staging_mask_splits = staging_mask.split('/')
        for checksum in keys:
            # print '\n', checksum
            duplist = map(lambda x: self.make_deduped_path(x), self.find_dups_for_checksum(checksum))
            duplist.sort
            photos_paths = []
            staging_paths = []
            for path in duplist:
                # print path
                if photos_mask in path:
                    photos_paths.append(path)
                elif staging_mask in path:
                    staging_paths.append(path)

            try:
                # if len(photos_mask) > 1:
                #     # raise Exception, 'more than 1 photo_path'
                #     print 'more than 1 photo_path'
                if len(staging_paths) < 1:
                    raise Exception, 'staging path not found'
            except Exception, msg:
                for pp in duplist:
                    print ' - ', pp
                raise Exception, msg

            dest = staging_paths[0]
            bucket = dest.split('/')[len(staging_mask_splits)]

            if bucket_list is None or bucket in bucket_list:

                # this is the expensive part ...
                if len(photos_paths) > 1:
                    print 'checking {} for file'.format(checksum)
                    dupset = DupSet(checksum, duplist)
                    source = dupset.get_dup_file()
                else:
                    source = photos_paths[0]
                shift_map.add(bucket, (source, dest))

        if 0:
            print '\nShiftMap'
            for key in shift_map.keys():
                print "- {} - {}".format(key, len(shift_map[key]))
                for pair in shift_map[key]:
                    print '\tsrc: {}\n\tdst: {}'.format(pair[0], pair[1])

        return shift_map

    def update_db_path(self, path, checksum, db):
        update_spec = {'path': path}
        where_clause = "WHERE check_sum = '{}'".format(checksum)
        db.update(update_spec, where_clause)

    def shift_file(self, src, dst):
        """
        1 - move the file from src to dst (try os.rename: is metadata preserved).
          - NOTE: we may have to create directories first
        2 - update record on composite to point to "ARCHIVE version of path (Staging)"
          - NOTE: this path should exist
        3 - update record on DE-DUP DB (with DE-DUP path)
          - note this record should exist
        :param src: source file (de-dup path) to be moved
        :param dst: destination path (may not exist)
        :return:
        """
        raise Exception, 'shif_file disabled'

        checksum = None

        # Error checking
        # First lets make sure the de-duped destination file does not already exist

        if not os.path.exists(src):
            msg = 'Shift source file does NOT exist at {}'.format(src)
            # raise Exception, msg
            print 'WARN: ', msg
            return
        if os.path.exists(dst):
            raise AlreadyProcessedException, 'Deduped dst file exists at {}'.format(dst)
            # os.remove(dst)

        archives_src_path = self.make_archives_path(src)
        archives_dst_path = self.make_archives_path(dst)

        # the file we will be pointing to in compositeDB should exist
        if not os.path.exists(archives_dst_path):
            raise ArchiveDstDoesNotExist, 'archives_dst_path does not exist at {}'.format(archives_dst_path)
            # pass

        # lets make sure we can find the record in Composite DB for this src path
        checksum = self.get_checksum_for_path(archives_src_path, self.composite_DB)
        print 'checksum:', checksum
        if checksum is None or checksum.strip() == '':
            raise Exception, 'Checksum not found for {}'.format(archives_src_path)


        ## Start nmaking mods to files and databases
        if 1:  # File Manipulations
            if not os.path.exists(os.path.dirname(dst)): # don't change path if file doesn't exist
                os.makedirs(os.path.dirname(dst))

            os.rename(src, dst)
            print 'moved to', dst

        # make a Archives version of the src file and find the entry in the Composite database
        if 1:  # composite DB.path.exists(archives_dst_path)
            if os.path.exists(archives_dst_path):
                self.update_db_path(archives_dst_path, checksum, self.composite_DB)

        if 1: # DE-Duped DB
            self.update_db_path(dst, checksum, self.dedupe_DB)

if __name__ == '__main__':
    dup_data_path = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'
    shifter = DupShifter(dup_data_path)

    dupsets = shifter.get_dupsets_containing ('CIC-ExternalDisk1/photos/')
    print len(dupsets), 'for Photos'

    # shifter.cache_dupsets_to_shift()
    shifter.report_cached_dupsets()

    # shifter.report_field_project_dupsets_containing_photos()

    if 0:  #m do shift
        skip_buckets = [
            'Field Project-ARISTO-FP21',
            'Field Project-BEACHON-FP13',
            'Field Project-DC3-FP19',
            'Field Project-DC3-FP22',
            'Field Project-ORCAS-FP21',
            'Field Project-PECAN-FP20',
            'SOARS-2',
            'SOARS-3',
        ]

        buckets = ['SOARS-3']
        shift_map = shifter.get_shift_map()
        print 'got shift map'
        for bucket in shift_map.keys():
            if bucket in skip_buckets:
                continue
            print '\n Processing', bucket
            items = shift_map[bucket]
            for i,item in enumerate(items):
                # print '\tsrc: {}\n\tdst: {}\n'.format(item[0], item[1])
                try:
                    shifter.shift_file(*item)
                except AlreadyProcessedException, msg:
                    print msg

                if i > 0 and i % 10 == 0:
                    print '{}/{}'.format(i, len(items))



