"""
We assume that the de-dup database points to the existing files in the de-duped file system

    (we can verify this with comms/cic_de_duped_verifer.py

NOTES:
    - Since CIC-ExternalDisk1/disc N directories have been processed, we can expect missing records there

We can use the database to de-dup database to generate lists of files that exist under a given directory.
We then test these paths to see if they participate in a dupset
    (using the path_map after casting the dup-path to an archives path)

If they are a dup, we can see if there is a better place for the dup file to be (say in Field Projects),
and move it accordingly using comms/dup_shifter.py

"""
import sys, os, re, traceback
from dup_finder import DupFinder
from comms.comms_db import CommsDBTable
from comms.dup_shifter import TallyDict, DupShifter, ArchiveDstDoesNotExist, AlreadyProcessedException

class DupComber (DupShifter):
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'

    def __init__(self, dup_data_path):
        DupShifter.__init__(self, dup_data_path)
        # self.db = CommsDBTable(self.sqlite_file)

    def get_comb_tally (self, basedir):
        path_map = self._get_path_map()
        records = self.dedupe_DB.select('path', "WHERE path LIKE '{}%'".format(basedir))
        paths = map (lambda x:x[0], records)
        print len(paths), 'paths found'
        candidates = [] # dupsets of the paths found
        comb_tally = TallyDict()
        for dedup_path in paths:
            archives_path = self.make_archives_path(dedup_path)
            if archives_path in path_map.keys():
                checksum = path_map[archives_path]
                print '\n', checksum, ' - ', dedup_path
                candidates.append(checksum)
                duplist = self.dup_map[checksum]
                duplist.sort()
                if 1:
                    for path in duplist:
                        if 1:
                            print '-', path
                            dest_dir = self.make_deduped_path(os.path.dirname(path))
                            comb_tally.add(dest_dir, dedup_path)
        return comb_tally

    def do_sweep (self, basedir):
        tally = self.get_comb_tally(basedir)
        for dedup_dest_dir in tally.keys():

            archive_src_paths = tally[dedup_dest_dir]
            for archive_src_path in archive_src_paths:
                dedup_src_path = self.make_deduped_path(archive_src_path)
                dedup_dest_path = os.path.join (dedup_dest_dir, os.path.basename(archive_src_path))
                print '\nsrc:', dedup_src_path
                print 'dst:', dedup_dest_path

                try:
                    self.shift_file(dedup_src_path, dedup_dest_path)
                    print 'SHIFTED!'
                except ArchiveDstDoesNotExist, msg:
                    print 'WARN:', msg
                except AlreadyProcessedException, msg:
                    print 'WARN:', msg
                except:
                    print traceback.print_exc()
                    sys.exit()

if __name__ == '__main__':
    dups_file = '/Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json'
    comber = DupComber(dups_file)

    base_cidr = '/Volumes/cic-de-duped/Field Projects/Field Project-PREDICT-FP17 (2011)'
    cdir = os.path.join (base_cidr, 'Disc 4/misc-1')
    cdir = os.path.join (base_cidr, 'Misc 1&2 Stills & raw files/disc1')

    if 0:
        comber.do_sweep(cdir)

    else:
        comb_tally = comber.get_comb_tally (cdir)
        print '\nDest Tally'
        total = 0
        for key in comb_tally.keys():
            print '-', key, ': ',len(comb_tally[key])
            if 0: # show each dup
                for p in comb_tally[key]:
                    print '\t',p
            total += len(comb_tally[key])

        print '\nTotal Dups found:', total

