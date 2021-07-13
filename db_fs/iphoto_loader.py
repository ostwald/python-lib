"""
deduping across iPhoto instances

mainly we want to change the way we handle suffix and file types (see extensions) ....

We want to skip files with no suffix or with "attr" suffix

"""
import os, sys
from walker import FSWalker, LoadingWalker, SafeLoadingWalker
import extensions

class IPhotoLoadingWalker (SafeLoadingWalker):

    accept_file_rules = [

        lambda x: os.path.splitext(os.path.basename(x))[1].lower() in extensions.ALL_TARGETS,
        lambda x: not os.path.islink((x)),
        # lambda x: 'hike' not in os.path.basename(x), # to not load files containing a string ('hike'
        # '[0-9A-Z]{8,}', # files that contain 8 or more consecutive caps_and_nums
    ]

    accept_dir_rules = [
        # lambda x: os.path.splitext(os.path.basename(x))[1].lower() == '.jpg',
        # return everything by default
        lambda x: os.path.basename(x)[0] != '.',
        # lambda x: os.path.basename(x) != 'NZ_2002',  # file name
        # lambda x: os.path.basename(x) != '2002',  # file name
    ]

def load_db_from_path (root, sqlitefile, safe=True):
    """

    :param root:
    :param sqlitefile:
    :param safe: the contents are not overwritten
    :return:
    """
    if not safe:
        if os.path.exists(sqlitefile):
            os.remove(sqlitefile)
            print 'removed dqlfile'
    # walker = LoadingWalker(root, sqlitefile)
    # walker = FSWalker(root)
    walker = IPhotoLoadingWalker(root, sqlitefile, safe)

    walker.walk()
    print '\n{}'.format(root)
    print 'all files: {}   loaded files: {}   dirs: {}  elapsed: {} millis'.format(
        walker.all_file_cnt, walker.file_cnt, walker.dir_cnt, '{:0.2f}'.format(walker.elapsed))
    # print 'unknown_extensions:', sorted (walker.unknown_extensions)
    print 'skipped_directories:', sorted (walker.skipped_directories)
    # if 0:
    #     print 'skipped directories'
    #     for d in walker.skipped_directories:
    #         print '-', d

def load_master_library():
    # base_dir = '/Volumes/enchilada/closet/in_process/iPhoto Library - mtSherman/Modified/2012/Aug 13, 2012_2'
    SAFE = 1
    base_dir = '/Volumes/enchilada/closet/iPhoto_7_Libraries/iPhoto Library/Originals'
    db_path = '/Users/ostwald/iPhoto_deduping/master_iphoto.sqlite'
    load_db_from_path (base_dir, db_path, SAFE)

def load_mt_sherman_library():
    SAFE = 1
    # base_dir = '/Volumes/enchilada/closet/in_process/iPhoto Library - mtSherman/Originals'
    # base_dir = '/Volumes/enchilada/closet/in_process/iPhoto Library - mtSherman/Modified/2012/Aug 13, 2012_2'
    db_path = '/Users/ostwald/iPhoto_deduping/mt_sherman_iphoto.sqlite'
    load_db_from_path (base_dir, db_path, SAFE)

def load_video_clips ():
    SAFE = 1
    base_dir = '/Volumes/enchilada/purg_home/Movies/VideoClips'
    db_path = '/Users/ostwald/iPhoto_deduping/video_clips.sqlite'
    load_db_from_path (base_dir, db_path, SAFE)

if __name__ == '__main__':


    load_video_clips()