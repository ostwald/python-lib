import os, sys, re, json, traceback
from comms.dup_manager import DupSet, DupManager
from comms import globals
from UserDict import UserDict

class NameDupManager (DupManager, UserDict):


    def __init__ (self, dup_data_path):
        """
        DupManager reads a json file containing a mapping from a key_value to set of dups.
            - the key_value is the value of the key field (e.g., the value of the key field)
            - dups are paths that are associated with key

        path_map - built as a side effect:( - maps the path of a file to it's key

        :param dup_data_path:
        """
        self.data_path = dup_data_path
        self.data = self.initialize_dup_data()
        print '{} dup entries found'.format(len (self.data))

        self.path_map = None
        self.dir_map = None

    def initialize_dup_data(self):
        return json.loads(open(self.data_path,'r').read())

    def get_dup_set (self, key):
        return DupSet (key, self.data[key])

    def _get_dir_map (self):
        """
        the dir_map collects the dups in a given collection. it is built by going through each dup and
        mapping it to the folder in which it lives. At the end, all the dups in a given folder collected.
        :return:
        """
        if self.dir_map is None:
            dir_map = {}

            for key in self.data.keys():
                dups = self.data[key]
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
            print 'PATH MAP DOING'
            path_map = {}
            if self.data is None:
                print 'WHAT? i am a {}'.format(self.__class__)
                sys.exit()
            for key in self.data.keys():
                for path in self.data[key]:
                    path_map[path] = key
            self.path_map = path_map
        return self.path_map

    def get_dupset (self, img_path=None, key=None):
        # print 'get_dupset'
        # print ' - img_path: {}'.format(img_path)
        # print ' - key: {}'.format(key)
        try:
            path_key = None
            if img_path is not None:
                path_key = self._get_path_map()[img_path]

            if key is not None and path_key is not None and path_key != key:
                raise Exception, "given check sum {} does not match derived key {}".format(key, path_key)
            dup_list = self.data[key]
            return DupSet (key, dup_list)
        except:
            traceback.print_exc()
            sys.exit()

    def report_dir_map(self, verbose=True):
        """
        produces a report that lists a folder, the number of dups vs the number of originals,
        and the individual dups if desired
        :return:
        """
        dir_map = self._get_dir_map()
        path_map = self._get_path_map()
        keys = sorted(dir_map.keys())
        for key in keys[:5]:
            dupfiles = dir_map[key]
            dup_files_cnt = len(dupfiles)
            # dir_img_cnt = len (globals.get_dir_iamges(dirname))
            # print '{} ({}/{})'.format(dirname, dup_files_cnt, dir_img_cnt)

            print '{}'.format(key)
            if verbose:
                for filename in dupfiles:
                    path = os.path.join (key, filename)
                    key_value = path_map[path]
                    print '- {}'.format(key_value)
                    # print '- ', filename
                    for dup in self.find_dups_for_file(path):
                        print '   -', dup

    def report_dups_in_folder(self, folder_path, level=0):
        """
        (recursively) lists the files in specified folder that have dups, and
         list the dups themselvesx

         NOTE and TODO - uses file system. Should be modified to use DataBase only!

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
            key = self._get_path_map()[path]
        except KeyError:
            print 'WARN: find_dups_for_file: path does not exist at {}'.format(path)
            return []

        dups = self.data[key]
        dups.remove(path)
        return dups

    def find_dups_for_key(self, key):
        return self.data[key]

    def find_disk_1_dups (self):
        """
        question: how many dups have at least one copy on CIC-ExternalDisk1?
        """
        return self.find_dups_with_substring('CIC-ExternalDisk1')

    def find_dups_with_substring (self, substr):
        """

        :param substr:
        :return: List of keys representing the dupsets containing the given substr
        """
        dup_set_keys = sorted(self.data.keys())

        selected_dup_sets = [] # these will have at least one copy on CIC-ExternalDisk1
        for key in dup_set_keys:
            dup_set = self.data[key]
            for dup in dup_set:
                if substr in dup:
                    selected_dup_sets.append (key)
                    break
        return selected_dup_sets

    def find_dup_items_with_substring (self, substr):
        """

        :param substr:
        :return: List of keys representing the dupsets containing the given substr
        """
        # dup_set_keys = sorted(self.data.keys())
        #
        # dup_items = [] # these will have at least one copy on CIC-ExternalDisk1
        # for key in dup_set_keys:
        #     dup_set = DupSet (key, self.data[key])
        #     print '-', key
        #     dup_items += dup_set.find_items_with_substring(substr)

        dup_items = []
        path_map = self._get_path_map()

        # print 'find_dup_items_with_substring'
        # print '  substring:', substr
        # print '  path_map: {}'.format(len(path_map))

        for path in path_map:
            if substr in path:
                dup_items.append(path)

        return dup_items


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
        # print ' - all paths: {} ({})'.format(len(all_paths), path)
        # non_dups = filter (lambda x: self.path_map.has_key(x), all_paths)

        non_dups = []
        path_map = self._get_path_map()
        for path in all_paths:
            if not path_map.has_key(path):
                non_dups.append(path)

        return non_dups

class BaseNameDupManager (NameDupManager):
    """
    the keys are the filenames without the extensions, making the idea
    of dup Names independent of extn.
    """

    def initialize_dup_data(self):
        dup_data = {}
        json_data = json.loads(open(self.data_path,'r').read())
        for filename_key in json_data.keys():
            basename_key = os.path.splitext(filename_key)[0]
            values = dup_data.has_key(basename_key) and dup_data[basename_key] or []
            values += json_data[filename_key]
            values.sort()
            dup_data[basename_key] = values
        return dup_data

if __name__ == '__main__':
    # print num_images_in_dir(foo)

    dup_data = '/Users/ostwald/Documents/Comms/Composite_DB/dups/file_name_dups.json'

    print dup_data
    ndm = BaseNameDupManager (dup_data)
    # ndm.report_dir_map()

    print 'NameDupManager'


    my_map = ndm  # ndm

    print '\nExample key and items'
    for my_key in my_map.keys()[:5]:
        print ' key: ',my_key
        print ' val: ', json.dumps(my_map[my_key], indent=3)

    # print '-  native: {} - {}'.format(len(ndm.keys()), ndm.keys()[0])
    # print '- dir_map: {} - {}'.format(len(dir_map.keys()), dir_map.keys()[0])
    # print '- path_map: {} - {}'.format(len(path_map.keys()), path_map.keys()[0])

    # print '{} paths in path_map'.format(len(path_map))
    #
    # print 'ndm has {} keys (e.g., "{}"'.format(len (ndm.keys()), ndm.keys()[0])