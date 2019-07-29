import os, sys, sqlite3, re
from report import TableReporter
import globals

"""
do reports over the top-level directories
- non-dups
- extension
"""

class CompositeReporter (TableReporter):

    folder_root = '/Volumes/archives/CommunicationsImageCollection/'

    def make_folder_path (self, rel_path):
        path = os.path.join (self.folder_root, rel_path)
        if not path.endswith('/'):
            path += '/'
        return path

    def get_count_for_extension (self, ext, folder):
        return self._get_scalar_for_extension('COUNT', ext, folder)

    def get_size_for_extension (self, ext, folder):
        return self._get_scalar_for_extension('SUM', ext, folder)

    def _get_scalar_for_extension (self, op, ext, folder):
        path = self.make_folder_path(folder)
        query = "SELECT {op} (size) FROM `{tn}` WHERE extension = '{tv}' AND path LIKE '{p}%'" \
            .format(op=op, tn=self.table_name, tv=ext, p=path)

        self.c.execute(query)
        return  self.c.fetchone()[0]

    def get_delimited_extension_count_report (self, delimiter='\t'):
        """
        columns are extensions
        rows are db_folders
        """
        return self._get_delimited_extension_report('count')

    def get_delimited_extension_size_report (self, delimiter='\t'):
        return self._get_delimited_extension_report('size')

    def _get_delimited_extension_report (self, op, delimiter='\t'):
        """
        columns are extensions
        rows are db_folders
        """
        if op == 'count':
            op_fn = self.get_count_for_extension
        elif op == 'size':
            op_fn = self.get_size_for_extension

        rows = []
        header = ['Folder', ] + self.get_unique_extensions()
        rows.append(header)
        for folder in globals.db_folder_names:
            row = [folder,]
            for ext in self.get_unique_extensions():
                # row.append (self.get_count_for_extension(ext, folder))
                val = op_fn(ext, folder)
                if op == 'size':
                    if val is None: val = 0
                    val = int(val/1000000)
                row.append(val)
            rows.append (map (lambda x:str(x), row))

        return '\n'.join(map (lambda r:'\t'.join (r), rows))


if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/Documents/Comms/Composite_DB/composite.sqlite'
    report_dir = '/Users/ostwald/Documents/Comms/Composite_DB/reports/'

    reporter = CompositeReporter (sqlite_file, report_dir)

    rpt = reporter.get_delimited_extension_count_report()
    print rpt

    rpt = reporter.get_delimited_extension_size_report()
    print rpt