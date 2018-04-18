"""
log grep -

for a given log file:
- compute start and end dates
- count the number of lines containing the specified strings
- report start and end dates, and grep counts

"""

import sys, os, datetime, re
from UserDict import UserDict

ts_pat = re.compile ("[A-Za-z]{3} [\d]*, [0-9]{4} [\d]*:[\d]*:[\d]* [A-Z]{2}")
adder_pat = re.compile ('\{add=\[([\S]*)')

not_found_str = '([A-Za-z]{3} [\d]{2} [\d]*:[\d]*:[\d]*) [A-Z]{3} '
not_found_str += '[\d]{4} Fedora Object ([\S]*)'
object_not_found_pat = re.compile(not_found_str)

# pattern: (tag, pattern_to_find)
patterns = (
    ('Start up', 'INFO: Starting service Catalina'),
    ('Shut down', 'INFO: Stopping service Catalina'),
    ('Out of Memory', 'java.lang.OutOfMemoryError: Java heap space'),
    ('Adder','{add=['),
    ('Broken Pipe','ClientAbortException:  java.net.SocketException: Broken pipe'),
    ('Connection Reset','ClientAbortException:  java.net.SocketException: Connection reset'),
    # ('Commit Flush','end_commit_flush'),
    ('OSWS Request', 'client=OpenSky+Web+Service'),
    ('OpenSky UI', '.keyDate.facet.date.gap'),
    ('NotFoundError', 'dk.defxws.fedoragsearch.server.errors.FedoraObjectNotFoundException'),
)

def make_header():
    fields = [];add=fields.append
    for attr in [
        'filename',
        'start_line',
        'end_line',
        'start_day',
        'start_ts',
        'end_ts',
        'startup',
        'shutdown',
    ]:
        add (attr)

    for key in [
        'Out of Memory',
        'Adder',
        'OSWS Request',
        'OpenSky UI',
        'Broken Pipe',
        'Connection Reset',
    ]:
        add (key)

    return '\t'.join(fields)

def get_datetime(datestr):
    return datetime.datetime.strptime(datestr, "%b %d, %Y %H:%M:%S %p")

def get_day(ts):
    dt = get_datetime(ts)
    return dt.strftime('%A')

def get_delta (d1, d2):
    """
    returns a timedelta object (absolute value)
    """
    return abs(get_datetime (d1) - get_datetime (d2))

def timetest():
    datestr1 = 'Mar 26, 2018 7:36:33 PM'
    datestr2 = 'Mar 26, 2018 7:38:33 PM'

    delta = get_delta(datestr1, datestr2)

    print delta.total_seconds()

def get_ts(line):
    m = ts_pat.match(line)
    if m:
        # print "MATCH %s" % m.group()
        return m.group()
    else:
        # print "no match"
        return None

def find_matched_pattern(line):
    for i, pat in enumerate(patterns):
        if line.find (pat[1]) > -1:
            return i
    return -1

class TallyRun (UserDict):

    def __init__ (self, filename):
        self.start_line = -1
        self.end_line = -1
        self.filename = filename
        self.start_ts = None  # first date
        self.start_day = None
        self.end_ts = None  # last date
        self.startup = '-' # tomcat startup timestamp
        self.shutdown = '-' # tomcat shutdown timestamp
        self.data = {}
        for pat in patterns:
            if pat[0] not in ['Start up', 'Shut down']:
                self[pat[0]] = 0

    def tally (self, tag):
        count = self.data.has_key(tag) and self[tag] or 0
        self[tag] = count + 1

    def report (self):
        print '\n%s (%d - %d)' % (self.filename, self.start_line, self.end_line)
        print 'tag tally'
        for key in sorted(self.keys()):
            print ' - %s: %d' % (key, self[key])
        print 'from: %s' % self.start_ts
        print 'to: %s' % self.end_ts
        print 'lines: %d' % (self.end_line - self.start_line)
        print 'start up: %s' % self.startup
        print 'shut down: %s' % self.shutdown


    def asTabDelimited (self):
        fields = [];add=fields.append
        for attr in [
            'filename',
            'start_line',
            'end_line',
            'start_day',
            'start_ts',
            'end_ts',
            'startup',
            'shutdown',
        ]:
            add (getattr(self, attr))

        for key in [
            'Out of Memory',
            'Adder',
            'OSWS Request',
            'OpenSky UI',
            'Broken Pipe',
            'Connection Reset',
        ]:
            add (self[key])

        return '\t'.join(map (str, fields))

class GrepTally (UserDict):

    max_lines = 50000000

    def __init__ (self, path):
        self.filename = os.path.basename(path)
        self.path = path
        self.data = {}
        self.runs = []
        self.lines = map (lambda x:x.strip(), open(self.path, 'r').read().split('\n'))
        print '%d lines read' % (len(self.lines))
        self.cur_run = TallyRun (self.filename)
        self.cur_run.start_line = 0
        self.runs.append(self.cur_run)
        self.process()



    def process(self):
        # data = [['line', 'timestamp', 'elapsed', 'tag'],]

        ct = None
        start_ts = None
        data = [['line', 'timestamp', 'tag'],]

        lines_to_process = min(len(self.lines), self.max_lines)

        print 'lines to process: %d' % lines_to_process

        for i, line in enumerate(self.lines[:lines_to_process]):

            if i>1 and i%10000 == 0:
                print '%d/%d' % (i, lines_to_process)
            if len(line) == 0: continue
            ts = get_ts(line)
            if ct is None:
                ct = ts
            if ts:
                ct = ts
                if self.cur_run.start_ts is None:
                    self.cur_run.start_ts = ct
                    self.cur_run.start_day = get_day(ct)

            pattern_index = find_matched_pattern(line)
            if pattern_index != -1:
                tag = patterns[pattern_index][0]
                if tag == 'Start up':
                    # update current run (with start/end date)

                    # reset data
                    # reset start_ts

                    self.handle_start_up(i, ct)
                elif tag == 'Shut down':
                    self.cur_run.shutdown = 'X'
                else:
                    self.cur_run.tally(tag)

        self.cur_run.end_line = i
        self.cur_run.end_ts = ct

    def handle_start_up(self, i, ct):
        self.cur_run.end_line = i
        self.cur_run.end_ts = ct


        # start a new tally
        self.cur_run = TallyRun (self.filename)
        self.cur_run.startup = 'X'
        self.cur_run.start_line = i
        self.cur_run.start_ts = ct
        self.cur_run.start_day = get_day(ct)
        self.runs.append(self.cur_run)

    def report (self):
        for run in self.runs:
            run.report()

    def asTabDelimited (self):
        rows=[];add=rows.append

        for run in self.runs:
            add (run.asTabDelimited())

        return '\n'.join(rows)


def write_data (outpath="/Users/ostwald/tmp/MASTER_LOG_GREP.txt"):
    fp = open(outpath, 'w')
    fp.write (make_header() + '\n')
    data_dir = '/Users/ostwald/Documents/OpenSky/logs/osstage2'

    # for filename in ['catalina.out-4_8-4_16',]:
    for filename in os.listdir(data_dir ):
        path = os.path.join (data_dir, filename)
        if not filename.startswith('catalina.out') or os.path.isdir(path) or filename[-1] == '~':
            continue
        tally = GrepTally(path)
        fp.write (tally.asTabDelimited() + '\n')

    fp.close()
    print 'wrote data to %s' % outpath

if __name__ == '__main__':

    if 0:
        path = '/Users/ostwald/Documents/OpenSky/logs/osstage2/catalina.out-4_8-4_16'
        tally = GrepTally (path)
        # tally.report()
        print tally.asTabDelimited()

    elif 1:
        write_data()
    else:
        line = 'dk.defxws.fedoragsearch.server.errors.FedoraObjectNotFoundException: Thu Apr 12 13:50:42 MDT 2018 Fedora Object articles:21423 not found at FgsRepos; nested exception is:'
        print 'not found tag: "%s"' % get_not_found_tag(line)