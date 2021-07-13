import os, sys
from comms import LoadingWalker, SafeLoadingWalker
import extensions


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
    # walker = LoadingWalker(root, sqlitefile)
    walker = SafeLoadingWalker(root, sqlitefile)
    walker.known_extentions = extensions.ALL_EXTENSIONS
    walker.target_extensions = extensions.ALL_TARGETS
    walker.skip_dir_names = extensions.SKIP_DIR_NAMES
    walker.skip_dir_name_frags = extensions.SKIP_DIR_NAME_FRAGS


    walker.walk()
    print '\n{}'.format(root)
    print 'all files: {}   loaded files: {}   dirs: {}  elapsed: {}'.format(walker.all_file_cnt, walker.file_cnt, walker.dir_cnt, walker.elapsed)
    print 'unknown_extensions:', sorted (walker.unknown_extensions)
    if 0:
        print 'skipped directories'
        for d in walker.skipped_directories:
            print '-', d


if __name__ == '__main__':

    # base_dir = '/Volumes/Video Backup'
    base_dir = '/Volumes/ostwald/Documents/Work'
    db_path = '/Users/ostwald/Documents/disk_mapping/foo.sqlite'
    load_db_from_path (base_dir, db_path)