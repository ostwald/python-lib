"""
make a mapping of dups per directory

    do some directories have all or mostly dups?

do all dups have same size (we better hope so)

which have different names (if any_?

"""
import os, sys, json
import globals


# def num_images_in_dir (dirname):
#     return len (globals.get_dir_iamges(dirname))

class DupAnalyzer:

    def __init__ (self, dup_data_path):
        """
        DupAnalyzer reads a json file containing a mapping from checksum to paths. So all the paths
        for a particular checksum are dups.

        path_map - built as a side effect:( - maps the path of a file to it's checksum

        :param dup_data_path:
        """
        self.dup_map = json.loads(open(dup_data_path,'r').read())
        print '{} dup entries found'.format(len (self.dup_map))

        self.path_map = None

        self.dir_map = None

    def _get_dir_map (self):
        """
        the dir_map collects the dups in a given collection. it is built by going through each dup and
        mapping it to the folder in which it lives. At the end, all the dups in a given folder collected.
        :return:
        """
        if self.dir_map is None:
            dir_map = {}

            for checksum in self.dup_map.keys():
                dups = self.dup_map[checksum]
                for d in dups:
                    dirname, filename = os.path.split(d)

                    items = dir_map.has_key(dirname) and dir_map[dirname] or []
                    items.append(filename)
                    dir_map[dirname] = items
            self.dir_map = dir_map
        return self.dir_map

    def _get_path_map (self):
        """
        invert dup_map
        """
        if self.path_map is None:
            path_map = {}
            for chksum in self.dup_map.keys():
                for path in self.dup_map[chksum]:
                    path_map[path] = chksum
            self.path_map = path_map
        return self.path_map

    def report_dir_map(self, verbose=True):
        """
        produces a report that lists a folder, the number of dups vs the number of originals,
        and the individual dups if desired
        :return:
        """
        dir_map = self._get_dir_map()
        path_map = self._get_path_map()
        keys = sorted(dir_map.keys())
        for dirname in keys:
            dupfiles = dir_map[dirname]
            dup_files_cnt = len(dupfiles)
            dir_img_cnt = len (globals.get_dir_iamges(dirname))
            print '{} ({}/{})'.format(dirname, dup_files_cnt, dir_img_cnt)
            if verbose:
                for filename in dupfiles:
                    path = os.path.join (dirname, filename)
                    checksum = path_map[path]
                    print '- {}  ({})'.format(filename, checksum)
                    # print '- ', filename
                    for dup in self.find_dups_for_file(path):
                        print '   -', dup

    def report_dups_in_folder(self, folder_path, level=0):
        """
        (recursively) lists the files in specified folder that have dups, and
         list the dups themselvesx
        """
        files = []
        dirs = []

        for filename in os.listdir(folder_path):
            path = os.path.join (folder_path, filename)
            if filename.startswith('.'): continue
            if os.path.isdir (path):
                dirs.append (path)
            else:
                # if this path is not in the path map then it is not a dup
                if self._get_path_map().has_key(path):
                    files.append (path)

        img_cnt = len (globals.get_dir_iamges(folder_path))
        print '\n{} - {}/{}'.format(folder_path, len(files), img_cnt)
        for path in files:
            print '- {}'.format(os.path.basename(path))
            dups = self.find_dups_for_file (path)
            for dup in dups:
                print '  - {}'.format(dup)
        for path in dirs:
            self.report_dups_in_folder (path, level+1)


    def find_dups_for_file (self, path):
        try:
            checksum = self._get_path_map()[path]
        except KeyError:
            print 'WARN: find_dups_for_file: path does not exist at {}'.format(path)
            return []

        dups = self.dup_map[checksum]
        dups.remove(path)
        return dups

    def find_disk_1_dups (self):
        """
        question: how many dups have at least one copy on CIC-ExternalDisk1?
        """
        dup_set_keys = sorted(self.dup_map.keys())

        selected_dup_sets = [] # these will have at least one copy on CIC-ExternalDisk1
        for checksum in dup_set_keys:
            dup_set = self.dup_map[checksum]
            for dup in dup_set:
                if "CIC-ExternalDisk1" in dup:
                    selected_dup_sets.append (checksum)
                    break
        return  selected_dup_sets

    def find_non_dups_for_directory (self, path, sqlite_file):
        """
        By finding the non_dups in a given directory we can get an idea
         of the amount of de-duping necessary
        """
        from comms_db import CommsDBTable
        db = CommsDBTable (sqlite_file)
        # print 'path:', path
        # print 'sqlite_file', sqlite_file
        all_paths = map(lambda x:x[0], db.select('path', "WHERE path LIKE '{}%'".format(path)))
        print 'all paths: {}'.format(len(all_paths))
        # non_dups = filter (lambda x: self.path_map.has_key(x), all_paths)

        non_dups = []
        path_map = self._get_path_map()
        for path in all_paths:
            if not path_map.has_key(path):
                non_dups.append(path)

        return non_dups

def non_dup_report (da):
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'
    root_path = "/Volumes/archives/CommunicationsImageCollection/"
    for name in globals.db_folder_names:
        path = os.path.join(root_path, name)
        print '\n',name
        non_dups = da.find_non_dups_for_directory (path, sqlite_file)
        print '{} non dups found'.format(len (non_dups))
        if 0:
            for nd in non_dups:
                print nd

def find_paths (da, needle, verbose=1):
    path_map = da._get_path_map()
    found = []
    for path in path_map.keys():
        if needle in path:
            found.append(path)
    print '{} found'.format(len(found))
    found.sort()
    if verbose:
        for p in found:
            print '-', p

if __name__ == '__main__':
    # foo = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk6/ignore these/predict'
    # print num_images_in_dir(foo)

    # dup_data = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk6/dups/check_sum_dups.json'
    # dup_data = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'
    # dup_data = '/Users/ostwald/tmp/TEST_composite/dups/check_sum_dups.json'
    # dup_data = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk1/dups/check_sum_dups.json'
    dup_data = '/Users/ostwald/Documents/Comms/Composite_DB/dups/check_sum_dups.json'

    da = DupAnalyzer (dup_data)
    # da.report_dir_map()

    path_map = da._get_path_map()
    print '{} paths in path_map'.format(len(path_map))

    find_paths(da, 'CarlyeMainDisk1/')

    if 0:
        # base_dir = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk6/archived/'
        base_dir = '/Volumes/archives/CommunicationsImageCollection/CIC-ExternalDisk1/design and work files'
        da.report_dups_in_folder(base_dir)


    if 0:
        total_cnt = len(da.dup_map)
        selected_dups = da.find_disk_1_dups()
        print 'total dup_sets: {}, dup_sets with at least one in ExternalDisk1: {}'.format(total_cnt, len(selected_dups))

    if 0:
        non_dup_report (da)

    if 0:
        sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'
        root_path = "/Volumes/archives/CommunicationsImageCollection/"
        folder = 'CIC-ExternalDisk7'
        path = os.path.join(root_path, folder)
        print '\n',folder
        non_dups = da.find_non_dups_for_directory (path, sqlite_file)
        print '{} non dups found'.format(len (non_dups))
        if 1:
            for nd in non_dups:
                print nd