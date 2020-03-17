"""
We have two dup files (json) and want to merge certain dupsets from one into another.

master dups - /Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json
- contains dup paths for files withing ExternalDisk1 (even though the files for all but
  one of the files should have been deleted

checksum dups - /Users/ostwald/Documents/Comms/Composite_DB/master_check_sum_dups.json
- the dup file created after merging Staging with Composite. This dups file contains many dups
 from Staging directories that we want to MERGE in with master_dups
"""

import sys, os, re, json
from comms.dup_manager import DupManager


def merge_dups (master_dup_mgr, new_dup_mgr):

    master_dups = master_dup_mgr.dup_map
    master_checksums = master_dups.keys()
    print '{} master_dup keys'.format(len(master_checksums))

    stage_dup_checksums = new_dup_mgr.find_dups_with_substring ('/Volumes/archives/CommunicationsImageCollection/Staging')
    print '{} stage_dups found'.format(len(stage_dup_checksums))

    if 1:
        for checksum in stage_dup_checksums:
            if master_dups.has_key(checksum):
                # print "collision"
                # print "Master Paths"
                master_paths = master_dups[checksum]
                # for p in master_paths:
                #     print '- {}'.format(p)

                # print "Stage Paths"
                for p in new_dup_mgr.dup_map[checksum]:
                    # print '- {}'.format(p)

                    if not p in master_paths:
                        master_paths.append(p)

                master_dups[checksum] = master_paths

                # print "MERGED PATHS"
                # for p in master_paths:
                #     print '- {}'.format(p)
            else:
                master_dups[checksum] = new_dup_mgr.dup_map[checksum]

    merged_dups_path = '/Users/ostwald/Documents/Comms/Composite_DB/dup_merger/MERGED_check_sum_dups.json'
    fp = open(merged_dups_path, 'w')
    fp.write (json.dumps(master_dups, indent=3))
    fp.close()
    print 'wrote to {}'.format(merged_dups_path)



if __name__ == "__main__":
    master_dup_mgr = DupManager('/Users/ostwald/Documents/Comms/Composite_DB/dup_merger/master_check_sum_dups.json')

    master_dups = master_dup_mgr.dup_map
    master_checksums = master_dups.keys()
    print '{} master_dup keys'.format(len(master_checksums))



    new_dup_mgr = DupManager('/Users/ostwald/Documents/Comms/Composite_DB/dup_merger/check_sum_dups.json')
    merge_dups (master_dup_mgr, new_dup_mgr)

    # stage_dup_checksums = new_dup_mgr.find_dups_with_substring ('/Volumes/archives/CommunicationsImageCollection/Staging')
    # print '{} stage_dups found'.format(len(stage_dup_checksums))
    #
    # if 1:
    #     for checksum in stage_dup_checksums:
    #         if master_dups.has_key(checksum):
    #             print "collision"
    #             print "Master Paths"
    #             master_paths = master_dups[checksum]
    #             for p in master_paths:
    #                 print '- {}'.format(p)
    #
    #             print "Stage Paths"
    #             for p in new_dup_mgr.dup_map[checksum]:
    #                 print '- {}'.format(p)
    #
    #                 if not p in master_paths:
    #                     master_paths.append(p)
    #
    #             master_dups[checksum] = master_paths
    #
    #             print "MERGED PATHS"
    #             for p in master_paths:
    #                 print '- {}'.format(p)
    #
    #