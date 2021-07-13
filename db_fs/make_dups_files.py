import os, sys, time
from comms import report
from comms.merge_db import CompositDB

# See the TableReporter methods - lots of reporting tools

def update_dup_files (sqlite_file):
    report_dir = os.path.dirname(sqlite_file)
    reporter = report.TableReporter(sqlite_file, report_dir)

    reporter.write_dup_reports()
    reporter.write_extension_report()

class DiskCompositeDB (CompositDB):

    comms_base = '/Users/ostwald/iPhoto_deduping'

    def find_dbs (self):
        dbs = [];add = dbs.append
        for filename in os.listdir(self.comms_base):
            if filename.endswith('.sqlite') and not 'composite' in filename:
                add (os.path.join (self.comms_base, filename))
                print ' - {}'.format(os.path.join (self.comms_base, filename))
        return dbs


def merge_databases (composite_sqlite_file):
    compositeDB = DiskCompositeDB(composite_sqlite_file)
    compositeDB.ingest_all()



if __name__ == '__main__':


    if 1:
        sqlite_file = '/Users/ostwald/iPhoto_deduping/composite.sqlite'
        update_dup_files(sqlite_file)


    if 0:
        composite_sqlite_File = '/Users/ostwald/iPhoto_deduping/composite.sqlite'
        # c = CompositDB(composite_sqlite_File)
        c = DiskCompositeDB(composite_sqlite_File)
        c.ingest_all()