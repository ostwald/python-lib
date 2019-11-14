import sys, os, re, time, json

import sqlite3

class TableReporter:

    table_name = 'comms_files'
    dup_fields = ['check_sum', 'file_name', 'size']

    def __init__ (self, db_path, report_dir):
        self.report_dir = report_dir
        self.sqlite_file = db_path
        self.dups_dir = os.path.join (self.report_dir, 'dups')
        self.unique_extensions = None
        if not os.path.exists(self.dups_dir):
            os.makedirs (self.dups_dir)
        conn = sqlite3.connect(self.sqlite_file)
        self.c = conn.cursor()

    def write_dup_reports (self):
        for field in self.dup_fields:
            self.write_dups(field)

    def get_distinct_values(self, field_name):

        # get total
        query = "SELECT DISTINCT ({fn}) FROM `{tn}` ".format(fn=field_name, tn=self.table_name)

        # print total_query

        self.c.execute(query)
        rows = self.c.fetchall()

        return map (lambda x:x[0], rows)

    def get_unique_extensions(self):
        if self.unique_extensions is None:
            self.unique_extensions =  self.get_distinct_values('extension')
        return self.unique_extensions

    def get_count_for_extension (self, ext):
        # get total
        query = "SELECT COUNT (extension) FROM `{tn}` WHERE extension = '{tv}'" \
            .format(tn=self.table_name, tv=ext)

        self.c.execute(query)
        return  self.c.fetchone()[0]

    def get_diskspace_for_extension (self, ext):
        # get total
        query = "SELECT SUM (size) FROM `{tn}` WHERE extension = '{tv}'" \
            .format(tn=self.table_name, tv=ext)

        self.c.execute(query)
        return  self.c.fetchone()[0]

    def extension_report (self):
        extensions = self.get_unique_extensions()
        extensions.sort()

        print 'Extension Diskspace'
        for ext in extensions:
            count = self.get_count_for_extension(ext)
            bytes = self.get_diskspace_for_extension(ext)

            # print '- {} : {} bytes'.format(ext,bytes)
            print '- {} - {} files - {} MB total'.format(ext, count, int(bytes/1000000))

    def get_extension_report_table (self):
        extensions = self.get_unique_extensions()
        extensions.sort()

        header = ['extension', 'num files', 'MB total']

        lines = [];add=lines.append
        add (header)
        total_MB = 0
        total_files = 0
        print 'Extension Diskspace'
        for ext in extensions:
            file_count = self.get_count_for_extension(ext)
            mega_bytes = int(self.get_diskspace_for_extension(ext)/1000000)

            add ([ext, str(file_count), str(mega_bytes)])

            total_files += file_count
            total_MB += mega_bytes

        add (['TOTAL', str(total_files), str(total_MB)])

        return lines


    def get_paths (self, field_name, field_value):
        """
        NOT USED
        :param field_name:
        :param field_value:
        :return:
        """
        # get total
        query = "SELECT path FROM `{tn}` WHERE {fn} = '{fv}'" \
            .format(tn=self.table_name, fn=field_name, fv=field_value)

        # print total_query

        self.c.execute(query)
        rows = self.c.fetchall()

        return map (lambda x:x[0], rows)

    # How to find all dups??
    def find_dups(self, field_name):
        """
        last_dup_value = None
        collected_paths = []
        for row in rows:
            dup_value = XX
            if dup_value != last_dup_value:
                if len(collected_paths > 1):
                    dups[last_dup_value] = collected_paths
                collected_paths = path
                last_dup_value = dup_value
            collected_paths.append(path)

        :param field_name:
        :return:
        """
        # get total
        query = "SELECT path, {fn} FROM `{tn}` ORDER BY {on}" \
            .format(tn=self.table_name, fn=field_name, on=field_name)

        self.c.execute(query)
        rows = self.c.fetchall()

        dup_map = {}
        last_value = None
        collected_paths = []
        for row in rows:
            dup_value = row[1]
            path = row[0]
            if dup_value != last_value:
                if len(collected_paths) > 1:
                    dup_map[last_value] = collected_paths
                collected_paths = [path,]
                last_value = dup_value
            else:
                collected_paths.append(path)
        if len(collected_paths) > 1:
            dup_map[last_value] = collected_paths
        return dup_map

    def get_delimited_extension_report (self, delimiter='\t'):
        """
        tab delimited can be pasted into spreadsheet
        :param delimiter:
        :return:
        """
        lines = self.get_extension_report_table()

        return '\n'.join (map (lambda x:delimiter.join (x), lines))

    def write_extension_report (self):
        csv = self.get_delimited_extension_report(',')
        db_name = os.path.splitext(os.path.basename(self.sqlite_file))[0]
        filename = '{}_extension_report.csv'.format(db_name)
        path = os.path.join (self.report_dir, filename)
        print 'sqlite_file: {}'.format(self.sqlite_file)
        print 'filename: {}'.format(filename)
        print 'report_dir: {}'.format(self.report_dir)
        print 'path: {}'.format(path)

        fp = open(path, 'w')
        fp.write (csv)
        fp.close()
        print 'wrote to {}'.format(path)

    def print_extension_report (self):
        """
        This can be cut and pasted into spreadsheet
        """
        print reporter.get_delimited_extension_report('\t')

    def write_dups (self, field):
        dups = self.find_dups(field)
        # dups_dir = '/Users/ostwald/Documents/Comms/comms_CIC-ExternalDisk1/dups'
        outpath = os.path.join (self.dups_dir, field + '_dups.json')
        fp = open(outpath, 'w')
        fp.write( json.dumps(dups, sort_keys=True, indent=4, separators=(',', ': ')))
        fp.close()
        print 'wrote dups to {}'.format(outpath)

    def count_results (self, where_clause="size > 10000 AND size < 20000"):

        query = "SELECT COUNT(path) FROM {} WHERE {}".\
            format(self.table_name, where_clause)

        self.c.execute(query)
        return  self.c.fetchone()[0]

def report_sqlite_dbs ():
    base_dir = '/Users/ostwald/Documents/Comms'
    for filename in os.listdir(base_dir):
        print filename
        if filename.startswith('.') or filename == 'FilemakerPro_DBs':
            continue
        sqlite_file = os.path.join (base_dir, filename, filename+'.sqlite')
        if not os.path.exists (sqlite_file):
            raise Exception, 'File not found at {}'.format(sqlite_file)
        report_dir = os.path.join (base_dir, filename)
        reporter = TableReporter(sqlite_file, report_dir)

        reporter.write_dup_reports()
        reporter.write_extension_report()

def report_db (sqlite_file, report_dir=None):
    print 'report_db'
    print 'sqlite_file:', sqlite_file
    print 'report_dir:', report_dir
    if report_dir is None:
        report_dir = os.path.dirname(sqlite_file)
    reporter = TableReporter(sqlite_file, report_dir)

    reporter.write_dup_reports()
    reporter.write_extension_report()


def report_composite ():
    # db_name = 'composite'
    # report_dir = '/Users/ostwald/Documents/Comms/Composite_DB'

    db_name = 'composite'
    report_dir = '/Users/ostwald/Documents/Comms/Composite_DB/'

    sqlite_file = os.path.join(report_dir, db_name + '.sqlite')

    reporter = TableReporter(sqlite_file, report_dir)
    reporter.write_dup_reports()
    reporter.write_extension_report()



if __name__ == '__main__':

    if 0:
        report_sqlite_dbs()

    if 0:
        report_composite()

    if 1:
        report_dir = '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped-reports'
        sqlite_file= '/Users/ostwald/Documents/Comms/Composite_DB/cic-de-duped.sqlite'
        report_db (sqlite_file, report_dir)

    if 0:
        sqlite_file = '/Users/ostwald/tmp/comms_db.sqlite'
        report_dir = '/Users/ostwald/tmp/reporter'
        reporter = TableReporter(sqlite_file, report_dir)

        # reporter.write_dup_reports()
        reporter.write_extension_report()


    if 0:  # size reporter
        sqlite_file = '/Users/ostwald/Documents/Comms/CIC-ExternalDisk1/CIC-ExternalDisk1.sqlite'
        report_dir = '/Users/ostwald/tmp/reporter'
        reporter = TableReporter(sqlite_file, report_dir)

        start = 0
        step = 2000

        while start < 1000000:
            end = start + step
            where = "size > {} AND size < {}".format(start, end)

            count = reporter.count_results (where)

            print "min: {}, max {}, count: {}".format(start, end, count)
            start = end

