"""
try to idendify directories of dups or derivatives

"""
import os, sys, sqlite3
from UserDict import UserDict
from comms_db import CommsDBTable
import globals
from dir_lister import list_img_spans

class FileEntry:

    def __init__ (self, file_data):
        self.path = file_data[0]
        self.size = file_data[1]
        self.filename = file_data[2]
        self.root, self.ext = os.path.splitext(self.filename)

class DirEntry:
    
    def __init__ (self, file_entry):
        self.path = os.path.dirname(file_entry.path)
        self.dirname = os.path.basename(self.path)
        self.files = []
        self.add_file (file_entry)

    def add_file (self, file_entry):
        self.files.append (file_entry)

    def get_avg_size (self):
        sum = 0
        for file in self.files:
            sum += file.size
        return int(sum/ 1000000 / len(self.files))

    def get_extensions (self):
        return list(set (map (lambda x:x.lower(), map (lambda x:x.ext, self.files))))

    def __repr__(self):
        s = self.dirname

        for file_entry in self.files:
            s += '\n\t{}'.format (file_entry.root)

        return s

    def __repr__ (self):
        s = '\n{}'.format(self.path)
        s += '\n {}'.format(list_img_spans(self.path))
        s += '\n avg size: {} MB'.format(self.get_avg_size())
        s += '\n extensions: {}'.format(','.join (self.get_extensions()))
        return s

class DirNameMap(UserDict):
    """
    keys are dirnames (e.g., 'tom arnold')
    values are lists of DirEntries
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


        # print 'path:', path
        # print 'filename', filename
        # print 'dirname', dirname
        
        # if self.data.has_key(dirname):
        #     self.data[dirname].add_file(file_entry)
        # else:
        #     entry = DirEntry (file_entry)
        #     self[entry.dirname] = entry

    def add_1 (self, path):
        dirpath, filename = os.path.split(path)
        dirname = os.path.basename(dirpath)
        # print '\npath:', path
        # print 'dirname:', dirname
        # print 'dirpath:', dirpath
        vals =  self.data.has_key (dirname) and self.data[dirname] or []
        if not dirpath in vals:
            vals.append (dirpath)
        self.data[dirname] = vals

class DirTool:

    def __init__ (self, sqlite_file):
        self.sqlite_file = sqlite_file

        conn = sqlite3.connect(self.sqlite_file)
        self.cursor = conn.cursor()
        self._file_entries = None
        self._dirname_map = None

    def get_dirname_map (self):
        if self._dirname_map is None:
            _dirname_map = DirNameMap()
            file_entries = self.get_file_entries()
            print '{} file_entries read'.format(len(file_entries))

            for file_entry in file_entries:
                _dirname_map.add (file_entry)

            self._dirname_map = _dirname_map
        return self._dirname_map

    def get_file_entries (self):
        if self._file_entries is None:
            query = "SELECT path, size, file_name FROM comms_files"

            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            # return map(lambda x:x[0], rows)
            self._file_entries =  map (FileEntry, rows)
        return self._file_entries

    def report_dirname(self, dirname):
        dir_entries = self.get_dirname_map()[dirname]
        print 'dir_entries is a {}'.format(type(dir_entries))
        for dir_entry in dir_entries:
            print dir_entry
            # print '\n', dir_entry.path
            # print list_img_spans(dir_entry.path)
            # print 'avg size: {} MB'.format(dir_entry.get_avg_size())
            # print 'extensions: {}'.format(','.join (dir_entry.get_extensions()))

def report_multies():
    sqlite_file = globals.composite_sqlite_file
    dt = DirTool(sqlite_file)
    dirname_map = dt.get_dirname_map()
    print '\ndirname_map has {} sets'.format(len(dirname_map))

    if 1:
        multies = 0
        for dirname in dirname_map.keys():
            dir_entries = dirname_map[dirname]
            if len(dir_entries) > 1:
                print '\n {} ({})'.format(dirname, len(dir_entries))
                for dir_entry in dir_entries:
                    print dir_entry.path
                multies += 1
        print 'There are {} Multies'.format(multies)

def report_dir_name (dirname):
    sqlite_file = globals.composite_sqlite_file
    dt = DirTool(sqlite_file)
    dirname_map = dt.get_dirname_map()
    print '\ndirname_map has {} sets'.format(len(dirname_map))
    dt.report_dirname(dirname)

if __name__ == '__main__':
    # report_multies()
    report_dir_name('Ana Ordonez')