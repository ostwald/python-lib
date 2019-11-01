"""
try to idendify directories of dups or derivatives

"""
import os, sys, sqlite3
from UserDict import UserDict
from comms_db import CommsDBTable
import globals
# from dir_lister import list_img_spans
from dir_lister_class import DBDirLister

__verbose__ = False

class FileEntry:

    def __init__ (self, file_data):
        self.path = file_data[0]
        self.size = file_data[1]
        self.filename = file_data[2]
        self.checksum = file_data[3]
        self.root, self.ext = os.path.splitext(self.filename)

class DirEntry:
    
    def __init__ (self, file_entry):
        self.path = os.path.dirname(file_entry.path)
        self.dirname = os.path.basename(self.path)
        self.files = []
        self._filename_map = {}

        self.add_file (file_entry)

    def get_file (self, filename):
        return self._filename_map[filename]


    def add_file (self, file_entry):
        self.files.append (file_entry)
        self._filename_map[file_entry.filename] = file_entry

    def get_avg_size (self):
        sum = 0
        for file in self.files:
            sum += file.size
        return int(sum/ 1000000 / len(self.files))

    def get_extensions (self):
        return list(set (map (lambda x:x.lower(), map (lambda x:x.ext, self.files))))

    def as_tab_delimited_record (self):
        """
        see DirTool.dir_header_fields
        """
        fields = [];add=fields.append
        add (self.dirname)
        add (self.path.replace ('/Volumes/archives/CommunicationsImageCollection/', ''))
        add (self.list_img_spans())
        add (len(self.files))
        add (self.get_avg_size())
        add (','.join (self.get_extensions()))
        return '\t'.join(map (lambda x:str(x), fields))

    def list_img_spans(self):
        lister = DBDirLister(self.path, recursive=False)
        return lister.list_img_spans()

    def is_dup_dir (self, other):
        """
        dup directories have the same number of files and the same checksums for each pair
        """
        if __verbose__:
            print self
            print other

        # do they have same number of files?
        if len (self.files) != len (other.files):
            # return False
            raise Exception ("different number of files")

        # does each file have dup counter part?
        for file in self.files:
            my_checksum = file.checksum
            other_file = other.get_file (file.filename)
            other_checksum = other_file.checksum
            if my_checksum != other_checksum:
                raise Exception ('checksum mismatch for {}'.format(file.filename))

        return True

    def __repr__ (self):
        s = '\n{}'.format(self.path)
        # s += '\n {}'.format(list_img_spans(self.path))
        s += '\n {}'.format(self.list_img_spans())
        s += '\n {} files'.format(len(self.files))
        s += '\n avg size: {} MB'.format(self.get_avg_size())
        s += '\n extensions: {}'.format(','.join (self.get_extensions()))
        return s

class DirNameMap(UserDict):
    """
    keys are dirnames (e.g., 'tom arnold')

    the values are lists of dir_entry_maps (that have the dirname of the key)

    dir_entry_map keys are directory paths, and the values are lists of files contained

    {
        "tom arnold" : [
            { "/some/path/tom arnold" : [
                "file_1.jpg",
                "file_2.jpg",
                ]
            },
            { "/some/other/tom arnold" : [
                ...
                ]
            }

    """

    def __init__(self):
        self.data = {}
        self.dir_entry_map = {}

    def add (self, file_entry):
        """
        dir dirname will be the key to this Map
        if the key (dirname) exists, see if there is a dirEntry with the same dirpath
        """
        dirpath = os.path.dirname(file_entry.path)
        dirname = os.path.basename(dirpath)

        # is there an entry for this directory name?
        if not self.has_key (dirname):
            self[dirname] = []

        # have we already created an DirEntry instance for this particular directory (dirpath)
        if self.dir_entry_map.has_key(dirpath):
            self.dir_entry_map[dirpath].add_file (file_entry)
        else:
            self.dir_entry_map[dirpath] = DirEntry (file_entry)
            self[dirname].append(self.dir_entry_map[dirpath])


    def get_dup_sets (self, dirname):
        dup_sets = []
        dir_entries = self.data[dirname]
        if len(dir_entries) < 2:
            return dup_sets

        while len(dir_entries) > 1:

            misses = []
            dups = []
            dir_entry_0 = dir_entries[0]
            for i in range (1, len(dir_entries)):
                dir_entry_i = dir_entries[i]
                try:
                    foo = dir_entry_0.is_dup_dir(dir_entry_i)
                    dups.append (dir_entry_i)
                except Exception, msg:
                    # print "not dup: {}".format(msg)
                    misses.append(dir_entry_i)

            if len(dups) > 0:
                dups.append (dir_entry_0)
                dup_sets.append (dups)
            dir_entries = misses


        return dup_sets

    def get_dup_sets_OLD (self, dirname):
        dup_sets = []
        dir_entries = self.data[dirname]
        print 'there are {} dir_entries'.format(len(dir_entries))
        if len(dir_entries) < 2:
            return dup_sets

        for i in range (0, len(dir_entries)-1):
            for j in range (i+1, len(dir_entries)):
                print 'i:{}, j:{}'.format(i,j)
                dir_entry_i = dir_entries[i]
                dir_entry_j = dir_entries[j]
                try:
                    dups = dir_entry_i.is_dup_dir(dir_entry_j)
                except Exception, msg:
                    print "not dup: {}".format(msg)
                    continue
                dup_sets.append ([dir_entry_i.path, dir_entry_j.path])
        return dup_sets


class DirTool:

    dir_header_fields = ['dirname', 'path', 'imgs ranges', 'num files', 'avg size (MB)', 'extensions']
    skip_dir_names = ['jpgs', 'raw files', 'extras', 'images', 'Untitled', 'tifs', 'tif files']

    def __init__ (self, sqlite_file):
        self.sqlite_file = sqlite_file

        conn = sqlite3.connect(self.sqlite_file)
        self.cursor = conn.cursor()
        self._file_entries = None  # a list of FileEntry
        self._dirname_map = None    # from dirname to [dirEntry]
        self._dirpath_map = None  # from path to dirEntry
        self._path_map = None     # from path to FileEntry

    def get_file_entry (self, path):
        return self.get_path_mao()[path]

    def get_dirname_map (self):
        """
        Build a map of all directory names to the FileEntries directly contained in the dir
        :return:
        """
        if self._dirname_map is None:
            _dirname_map = DirNameMap()
            file_entries = self.get_file_entries()
            # print '{} file_entries read'.format(len(file_entries))

            for file_entry in file_entries:
                _dirname_map.add (file_entry)

            self._dirname_map = _dirname_map
        return self._dirname_map

    def get_dir_entry (self, path):
        return self.get_dirpath_map()[path]

    def get_dirpath_map (self):
        if self._dirpath_map is None:
            _dirpath_map = {}
            dirname_map = self.get_dirname_map()

            for key in dirname_map.keys():
                entries = dirname_map[key]
                for dir_entry in entries:
                    _dirpath_map[dir_entry.path] = dir_entry

            self._dirpath_map = _dirpath_map
        return self._dirpath_map

    def get_path_map (self):
        if self._path_map is None:
            _path_map = {}
            for entry in self.get_file_entries():
                _path_map[entry.path] = entry
            self.path_map = _path_map
        return self._path_map

    def get_file_entries (self):
        """
        fetch ALL entries from the database as FileEntry instances
        """
        if self._file_entries is None:
            query = "SELECT path, size, file_name, check_sum FROM comms_files"

            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            # return map(lambda x:x[0], rows)
            self._file_entries =  map (FileEntry, rows)
        return self._file_entries

    def report_dir_name(self, dirname):
        dir_entries = self.get_dirname_map()[dirname]
        for dir_entry in dir_entries:
            print dir_entry

    def dir_entry_as_tab_delimited_records(self, dirname):
        records = [];add=records.append
        dir_entries = self.get_dirname_map()[dirname]
        for dir_entry in dir_entries:
            add (dir_entry.as_tab_delimited_record ())
        return records

    def get_multies (self, filter_fn):
        """
        only report mulities that have at least on dir that satsifies filter

        returns a list of dirnames (from which we get the individual dir_entries for display, etc)
        :return:
        """
        dirname_map = self.get_dirname_map()
        print '\ndirname_map has {} sets'.format(len(dirname_map))

        multies = 0
        keys = dirname_map.keys()
        # keys.sort (key = lambda x:-len(dirname_map[x]))
        keys.sort (key = lambda x:x.upper())
        # for dirname in dirname_map.keys():
        multies = []
        for dirname in keys:
            if dirname in self.skip_dir_names:
                continue

            # we want more than one dir AND at least one dir that satisfies filter)

            dir_entries = dirname_map[dirname]
            if len(dir_entries) > 1:
                filtered_dir_entries = filter (filter_fn, dir_entries)
                if len(filtered_dir_entries) > 0:
                    multies.append(dirname)
        return multies

    def report_multies(self, filter_fn=None, display_fn=None):
        """
        only report mulities that have at least on dir that satsifies filter
        :return:
        """
        multies = self.get_multies(filter_fn=filter_fn)
        dirname_map = self.get_dirname_map()
        for dirname in multies:
            dir_entries = dirname_map[dirname]

            print '\n{}\n{}\n '.format('-'*50, dirname)
            # self.report_dir_name(dirname)
            print dir_entries

        print '\n{} multies found'.format(len(multies))

    def get_multi_csv(self, filter_fn=None):

        multies = self.get_multies(filter_fn=filter_fn)

        lines = []
        lines.append ('\t'.join(self.dir_header_fields))

        dirname_map = self.get_dirname_map()
        keys = dirname_map.keys()
        # keys.sort (key = lambda x:-len(dirname_map[x]))
        keys.sort (key = lambda x:x.upper())

        for dirname in multies:
            lines = lines + self.dir_entry_as_tab_delimited_records(dirname)
        return '\n'.join(lines)


    def write_multi_report(self, outpath="MULTI_TAB_DELIMITED.txt", filter_fn=None):
        txt = self.get_multi_csv(filter_fn=filter_fnb)
        fp = open (outpath, 'w')
        fp.write(txt)
        fp.close()
        print 'wrote to {}'.format(outpath)


    def get_dup_sets (self, filter_fn=None):
        multies = self.get_multies(filter_fn)
        dirname_map = self.get_dirname_map()
        dup_sets = []
        for dirname in multies:
            dup_sets = dup_sets + dirname_map.get_dup_sets(dirname)
            # print '{} -- {}'.format(dirname, len(dup_sets))
        return dup_sets

    def write_dup_sets_report(self, outpath="DUP_SETS_FROM_MULTIES.txt", filter_fn=None):
        dup_sets = self.get_dup_sets(filter_fn=filter_fn)
        fp = open (outpath, 'w')
        fp.write ('\t'.join(self.dir_header_fields) + '\n')
        for dup_set in dup_sets:
            for dup in dup_set:
                fp.write (dup.as_tab_delimited_record() + '\n')
            fp.write ('\n')
        fp.close()
        print 'wrote to {}'.format(outpath)

def report_dir_name (dirname):
    sqlite_file = globals.composite_sqlite_file
    dt = DirTool(sqlite_file)
    dirname_map = dt.get_dirname_map()
    # print '\ndirname_map has {} sets'.format(len(dirname_map))
    dt.report_dir_name(dirname)

def is_dup_dir_tester():
    sqlite_file = globals.composite_sqlite_file
    dt = DirTool(sqlite_file)
    # dt.report_multies (filter_fn = lambda x: "CIC-ExternalDisk6" in x.path)
    # print dt.get_multi_csv(filter_fn=filter_fn)

    # path1 = globals.make_path('CIC-ExternalDisk7/bob%27s photos exported/katharine hayhoe - WOR lecture')
    # path2 = globals.make_path('CIC-ExternalDisk7/bob%27s photos exported/Katharine Hayhoe-WOR lecture-9.5.14')

    path1 = globals.make_path('CIC-ExternalDisk7/Images from Bob%27s hard drive/Lower-priority pix--removed from Bob%27s hard drive (all by BH, (c) UCAR)/VORTEX2 6.09')
    path2 = globals.make_path('CIC-ExternalDisk6/ignore these/vortex2/bobs photos')
    dir1 = dt.get_dir_entry(path1)
    dir2 = dt.get_dir_entry(path2)




if __name__ == '__main__':
    # report_multies()
    # report_dir_name('Ana Ordonez')
    # report_filtered_multies(lambda x: "CIC-ExternalDisk6" in x.path)

    filter_fn = lambda x: "CIC-ExternalDisk6" in x.path

    sqlite_file = globals.composite_sqlite_file
    dt = DirTool(sqlite_file)


    dt.write_dup_sets_report (filter_fn=None)



    # multies = dt.get_multies(filter_fn=filter_fn)
    # for m in multies:
    #     print '\n{}\n '.format('-'*50)
    #     for dir_entry in m:
    #         print dir_entry
    #
    # print '{} multies found'.format(len(multies))



    # dt.report_multies (filter_fn=filter_fn)
    # print dt.get_multi_csv (filter_fn=filter_fn)

