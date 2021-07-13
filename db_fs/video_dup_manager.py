import sys, os
import shutil
import traceback
from comms import DupManager, CommsDBTable

MT_SHERMAN_PATH = '/Volumes/enchilada/closet/in_process/iPhoto Library - mtSherman'
VIDEO_CLIPS_PATH = '/Volumes/enchilada/purg_home/Movies/VideoClips'
MASTER_PATH = '/Volumes/enchilada/closet/iPhoto_7_Libraries/iPhoto Library'

VIDEO_EXTNS = [
    '.mov',
    '.avi',
    '.dv',
    '.mp4',
    '.m4v',
    '.wmv',
]

def get_video_where_clause ():
    clauses = []
    for extn in VIDEO_EXTNS:
        # print extn
        clause = "file_name LIKE '%{}'".format(extn)
        clauses.append(clause)
    return ' or '.join (clauses)

def is_video (path):
    try:
        return os.path.splitext(path)[1].lower() in VIDEO_EXTNS
    except:
        return False

class VideoDupManager (DupManager):

    dowrites = 0
    verbose = 0
    empty_file_checksum = 'd41d8cd98f00b204e9800998ecf8427e'



    def __init__ (self, dup_data_path, sqlite_file):
        """
        self.dup_map, which mapps a checksum to the fileset for that checksum

        """
        self.dup_data_path = dup_data_path
        self.sqlite_file = sqlite_file
        self.db = CommsDBTable (sqlite_file)
        DupManager.__init__(self, dup_data_path)
        print 'initialized with {}'.format(len(self.dup_map))
        self.filter_for_videos()
        print 'filtered to {}'.format(len(self.dup_map))

        self.to_delete = None

    def filter_for_videos (self):
        dup_video_map = {}
        for key in self.dup_map.keys():
            dupset = self.dup_map[key]
            video_dup_set = []
            for dup_path in dupset:
                if is_video(dup_path):
                    video_dup_set.append(dup_path)
            if len(video_dup_set) > 1:
                dup_video_map[key] = video_dup_set
        self.dup_map = dup_video_map


    def default_process_dupset(self, checksum):
        print 'default_process_dupset: {}'.format(checksum)
        return 1

    def get_non_dups (self, path):
        """
        1 - collect all paths that contain path
        2 - remove paths that are duplicates
        :param path:
        :return: non-dups with paths starting with the provided path
        """
        all_paths = map(lambda x:x[0], self.db.select('path', "WHERE path LIKE '{}%'".format(path)))
        print ' - all paths: {} ({})'.format(len(all_paths), path)
        # non_dups = filter (lambda x: self.path_map.has_key(x), all_paths)

        non_dups = []
        path_map = self._get_path_map()
        for path in all_paths:
            if not path_map.has_key(path):
                non_dups.append(path)
        return non_dups

    def process_dupset(self, checksum):
        if 0 and self.verbose:
            print 'process_dupset: {}'.format(checksum)
        dup_set = self.dup_map[checksum]

                # Here is the way we can collect paths using a predicate such as 'in'
#        backup_paths = filter (lambda x:'Video Backup' in x, dup_set)

        mt_sherman_paths = filter (lambda x:x.startswith (MT_SHERMAN_PATH), dup_set)
        video_clips_paths = filter (lambda x:x.startswith (VIDEO_CLIPS_PATH), dup_set)
        master_paths = filter (lambda x:x.startswith (MASTER_PATH), dup_set)
        if mt_sherman_paths and video_clips_paths and master_paths:
            print '\n{}'.format(checksum)
            print '- {}/{} mt sherman paths'.format(len(mt_sherman_paths), len(dup_set))
            print '- {}/{} video clips paths'.format(len(video_clips_paths), len(dup_set))
            print '- {}/{} master paths'.format(len(master_paths), len(dup_set))

        return 1

    def process_dupsets (self, fn=None):
        """
        backup_dupsets are like
        - /Volumes/Video Backup/Video/AccessQuality/HD/2011-01-09 - 2011-01-15/00048.mp4
        - /Volumes/VideoLibrary/Video/AccessQuality/HD/2011-01-09 - 2011-01-15/00048.mp4

        :return:
        """
        if fn is None:
            # fn = self.default_process_dupset
            fn = self.process_dupset

        # for dup_set in reporter.dup_map.values():
        checksums = self.dup_map.keys()

        self.to_delete = []
        for checksum in checksums:

            # the call is GET_BACKUP_PATH

            # where it should be
            # if call returns true
            #   then append to whatever
            #   print whatever

            try:
                if fn (checksum) and self.verbose:
                    print 'success processed dupset for {}'.format(checksum)
            except:
                if self.verbose:
                    print 'fail with checksum {}'.format(checksum)
                    traceback.print_exc()

        # Now loop through the "to_delete" paths
        for path_to_delete in self.to_delete:

            if self.dowrites:

                # DB delete (path_to_delete)
                try:
                    where_condition = "path = '{}'".format(path_to_delete)
                    self.db.delete_record(where_condition)
                except:
                    traceback.print_exc()
                    sys.exit()
            else:
                print 'woulda deleted ', path_to_delete

class ReportingVideoDupManager (VideoDupManager):

    def __init__ (self, dup_data_path, sqlite_file):
        self.video_dup_sets = []
        VideoDupManager.__init__ (self, dup_data_path, sqlite_file)

    def process_dupset(self, checksum):
        dup_set = self.dup_map[checksum]
        for path in dup_set:
            name, ext = os.path.splitext(os.path.basename(path))
            if ext.lower() in VIDEO_EXTNS:
                self.video_dup_sets.append (checksum)
                break
        return 1

    def report_dupsets (self):
        self.process_dupsets()
        print 'There are {} dupsets out of {} videos in {}'.format(len(self.video_dup_sets),
                                                        len(self.dup_map.keys()),
                                                        os.path.basename(self.sqlite_file))
         # print 'There are {} dups in {}'.format(len(self.dup_map.keys()), os.path.basename(self.sqlite_file))
        if 0:  # show the dupsets
            for checksum in self.video_dup_sets:
                dup_set = self.dup_map[checksum]
                print ''
                for path in dup_set:
                    print path

    def report_paths (self):
        #  dupes, and non-dups in the different datasets: VIDEO_CLIPS_PATH, MT_SHERMAN_PATH, MASTER_PATH
        paths = [VIDEO_CLIPS_PATH, MT_SHERMAN_PATH, MASTER_PATH]
        for path in paths:
            print '\n', path
            non_dups = filter (is_video, self.get_non_dups(path))
            print '  {} non-dups'.format(len(non_dups), path)

            dup_paths = self.find_dup_items_with_substring(path)
            print '  {} dup items'.format(len(dup_paths))

    def report_path (self, path):
        non_dups = filter (is_video, self.get_non_dups(path))
        print '  {} non-dups'.format(len(non_dups), path)
        non_dups.sort()
        for i, nd_path in enumerate(non_dups):
            # print i,'-', nd_path
            pass

        dup_paths = self.find_dup_items_with_substring(path)
        print '  {} dup items'.format(len(dup_paths))
        dup_paths.sort()
        for path in dup_paths:
            print '-', path



    def report (self):
        pass

    def test_for_unique_filenames (self, paths):
        uniques_names = []
        dup_names = []
        for path in paths:
            name = os.path.basename(path)
            if name in uniques_names:
                dup_names.append(name)
            else:
                uniques_names.append(name)

        # print '{} dup_names'.format(len(dup_names))
        # print '{} uniques_names'.format(len(uniques_names))
        if len(dup_names) > 0:
            raise Exception, 'Duplicate names ({})'.format(len(dup_names))

    def write_mt_sherman_non_dups(self, path, dest_dir=None):
        if dest_dir is None:
            dest_dir="/Users/ostwald/Movies/Mt_sherman_non_dups"

        # we'd like to keep the same filenames - let's see if there are dups
        video_paths = filter(is_video, self.get_non_dups(path))
        print '{} video_paths to write'.format(len(video_paths))

        # raise error if there are duplicate namesa among the video_paths
        self.test_for_unique_filenames (video_paths)

        for src in video_paths:
            filename = os.path.basename(src)
            dest = os.path.join (dest_dir, filename)
            print dest
            if not os.path.exists(dest):
                shutil.copy2(src,dest)




if __name__ == '__main__':
    data_path = '/Users/ostwald/iPhoto_deduping/dups/check_sum_dups.json'
    sqlite_file = '/Users/ostwald/iPhoto_deduping/composite.sqlite'
    vdm = ReportingVideoDupManager (data_path, sqlite_file)

    # dup_paths = vdm.find_dup_items_with_substring(MT_SHERMAN_PATH)
    # print '{} dup_paths'.format(len(dup_paths))

    # vdm.report_dupsets()
    # vdm.report_paths()
    # vdm.report_path(MT_SHERMAN_PATH)
    # vdm.report()

    vdm.write_mt_sherman_non_dups(MT_SHERMAN_PATH)



