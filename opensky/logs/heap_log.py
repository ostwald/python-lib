"""
use time stamps in file to try and identify major out of memory episodes
as well as singletons

first of all, march down the lines in a log file keeping track of the last date read
(this running date will be used as approx timestamp for error messages, which often
do not have a timestamp
"""

import sys, os, datetime, re

ts_pat = re.compile ("[A-Za-z]{3} [\d]*, [0-9]{4} [\d]*:[\d]*:[\d]* [A-Z]{2}")
adder_pat = re.compile ('\{add=\[([\S]*)')

not_found_str = '([A-Za-z]{3} [\d]{2} [\d]*:[\d]*:[\d]*) [A-Z]{3} '
not_found_str += '[\d]{4} Fedora Object ([\S]*)'
object_not_found_pat = re.compile(not_found_str)

# pattern: (tag, pattern_to_find)
patterns = (
    # ('Start up', 'INFO: Starting service Catalina'),
    # ('Shut down', 'INFO: Stopping service Catalina'),
    ('Shut down', 'INFO: Pausing Coyote HTTP/1.1 on http-8080'),
    # ('Out of Memory', 'java.lang.OutOfMemoryError: Java heap space'),
    # ('Adder','{add=['),
    # ('Broken Pipe','ClientAbortException:  java.net.SocketException: Broken pipe'),
    # ('Connection Reset','ClientAbortException:  java.net.SocketException: Connection reset'),
    # ('Commit Flush','end_commit_flush'),
    # ('OSWS Request', 'client=OpenSky+Web+Service'),
    # ('OpenSky UI', '.keyDate.facet.date.gap'),
    # ('NotFoundError', 'dk.defxws.fedoragsearch.server.errors.FedoraObjectNotFoundException'),
)

def get_datetime(datestr):
    return datetime.datetime.strptime(datestr, "%b %d, %Y %H:%M:%S %p")

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
    for i, pat in enumerate(patterns):f
        if line.find (pat[1]) > -1:
            return i
    return -1

def process(path):
    # data = [['line', 'timestamp', 'elapsed', 'tag'],]
    data = [['line', 'timestamp', 'tag'],]
    lines = map (lambda x:x.strip(), open(path, 'r').read().split('\n'))

    print '%d lines read' % (len(lines))

    ct = None
    max_lines = 5000

    lines_to_process = min(len(lines), max_lines)

    for i, line in enumerate(lines[:lines_to_process]):
        if i>1 and i%10000 == 0:
            print '%d/%d' % (i, lines_to_process)
        if len(line) == 0: continue
        ts = get_ts(line)
        if ct is None: ct = ts
        if ts:
            # print '- %d - %s' % (i, ts)
            delta = get_delta (ct, ts)
            ct = ts

        pattern_index = find_matched_pattern(line)
        if pattern_index != -1:
            tag = patterns[pattern_index][0]
            if tag == 'Adder':
                tag = get_adder_tag (line)
            if tag == 'NotFoundError':
                tag = get_not_found_tag(line)
            if 1 or delta > datetime.timedelta(minutes=0):
                # print  '- %d - %s (%s) - %s' % (i, ct, delta, tag)
                # data.append([i, ct, delta, tag])
                data.append([i, ct, tag])

    return data

def get_adder_tag (line):
    m = adder_pat.search(line)
    if m:
        return 'Adder - ' + m.group(1)
    else:
        return 'Adder'

def get_not_found_tag (line):
    tag = "401(unauthorized)"
    m = object_not_found_pat.search(line)
    if m:
        return '%s - %s' % (tag, m.group(2))
    else:
        return '%s - ??' % tag

def write_data (data, outpath="HEAP_LOG_DATA.txt"):
    fp = open(outpath, 'w')

    for entry in data:
        fp.write ('\t'.join(map(str, entry)) + '\n')
    fp.close()
    print 'wrote data to %s' % outpath

if __name__ == '__main__':

    if 0:
        path = '/Users/ostwald/Documents/OpenSky/logs/osstage2/catalina.out-4_8-4_16'
        data = process (path)
        # print 'data is %d lines' % len (data)
        # print data
        print '%d lines selected' % len (data)
        # for d in data:
        #     print d

        # outpath = 'output/' + os.path.splitext(os.path.basename(path))[0] +'.txt'
        # outpath = 'output/' + os.path.basename(path) +'.txt'
        # write_data(data, outpath)
    elif 1:
        ts1 = 'Apr 12, 2018 6:00:01 AM'
        ts2 = 'Apr 12, 2018 7:00:02 AM'
        delta = get_delta (ts1, ts2)
        print 'delta: ', delta
        if delta > datetime.timedelta(hours=1):
            print 'bigger than an hour'
        else:
            print 'smaller than an hour'
    else:
        line = 'dk.defxws.fedoragsearch.server.errors.FedoraObjectNotFoundException: Thu Apr 12 13:50:42 MDT 2018 Fedora Object articles:21423 not found at FgsRepos; nested exception is:'
        print 'not found tag: "%s"' % get_not_found_tag(line)