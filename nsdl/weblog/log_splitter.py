"""
split a log file up into a bunch of individual files by day.

per-day files written to directory specified by "baseDir"
"""
import os, sys, re
from log_file import LogFile

class LogSplitter(LogFile):
    """
    parses a log file into a list of entries

    splits the log file into entries for each day/date, and then writes
    the entries for each day into a log file in "splitsDir"
    """

    def __init__ (self, path, splitsDir):
        self.splitsDir = splitsDir
        self.split_cnt = 0
        LogFile.__init__ (self, path)
        if not os.path.exists(self.splitsDir):
            os.mkdir(self.splitsDir)

    def split (self):
        """
        process the lines/entries of the log file, writing the entries for each
        day into its own file
        """
        entries = []
        current_date = self[0].date
        for line in self:
            mydate = line.date
            if mydate == current_date:
                entries.append(line.data)
            else:
                # print 'would have written %d entries with date = %s' % (len(entries), current_date)
                self.writeEntries(entries)
                current_date = mydate
                entries = []
        if entries:
                # print 'would have written %d entries with date = %s' % (len(entries), current_date)
                self.writeEntries(entries)


    def writeEntries (self, entries):
        self.split_cnt += 1
        filename = '%s.%d' % (self.baseFilename, self.split_cnt)
        outpath = os.path.join (self.splitsDir, filename)
        fp = open(outpath, 'w')
        fp.write ('\n'.join(entries))
        fp.close()
        print 'wrote to', outpath
                
if __name__ == '__main__':
    if 0:
        path = '/home/ostwald/logs/log_files/harvest.nsdl.org_access_log'
        dest = '/home/ostwald/logs/harvest_logs'
    if 1:
        path = '/home/ostwald/logs/log_files/ns.nsdl.org_access_log'
        dest = '/home/ostwald/logs/ns_logs'


    log = LogSplitter (path, dest)
    print '%d lines read' % len(log)

    log.split()
