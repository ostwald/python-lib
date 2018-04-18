import sys, os, re, time
from UserDict import UserDict
from UserList import UserList
from urlparse import urlparse, parse_qs

# 184.106.66.249 - - [01/Nov/2017:00:32:10 -0600] "GET /front_page_announcements/front_page_announcements_default_live.html

class LogEntry:
    """
    encapsulate a line of the weblog
    """

    pat = pat = re.compile('([.0-9]*) - - \[(.*) -[0-9]*\]* \"([A-Z]*) ([^ ]*) .*')
    
    def __init__(self, line):

        m = self.pat.match (line)
        if not m:
            raise Exception, 'Unparseable: %s' % line
        self.ip = m.group(1)
        self.date = self.fmt_date(m.group(2))
        self.method = m.group(3)
        self.path = m.group(4)
        self.params = None

    def __repr__ (self):
        attrs = ['ip', 'date', 'method', 'path']
        vals = map(lambda x:getattr(self, x), attrs)
        return ' - '.join(vals)

    def fmt_date (self, entry_date):
        log_fmt = '%d/%b/%Y:%H:%M:%S'
        date = time.strptime(entry_date, log_fmt)
        
        fmt_out = '%Y-%m-%d'
        
        return time.strftime(fmt_out, date)

    def get_query_param (self, param_name):
        if self.params is None:
            parse = urlparse(self.path)
            self.params = parse_qs(parse.query)
        if not self.params.has_key(param_name):
            return None
        param = self.params[param_name]
        if type(param) == type([]) and len(param) == 1:
            return param[0]
        return param

class TrackingEntry (LogEntry):

    def __init__ (self, line):
        super(TrackingEntry, self).__init__(self, line)
        
class LogFile (UserList):

    def __init__ (self, path):
        self.data = []
        lines = open(path, 'r').read().split('\n')
        print '%d lines read' % len (lines)
        for line in lines:
            try:
                entry = LogEntry(line)
                self.append(entry)
            except:
                # print 'Error: %s' % sys.exc_info()[1]
                pass
        print '\n%d Entries read' % len (self.data)

def LogFileTester ():
    path = '/Users/ostwald/tmp/ccs-nov-dec.log'
    lf = LogFile(path)
    #find entries for a specific path
    # login_lines = filter (lambda x:x.path.find ('/home/login/verify.do') > -1, lf.data)
    login_lines = filter (lambda x:x.path.startswith ('/home/tr/ct.js'), lf.data)

    print '%d filtered entries' % len(login_lines)
    for l in login_lines[:10]:
        print l.path, l.get_query_param('uuid')

def make_tally():
    """
    print out unique ip visitors over log
    """
    path = '/Users/ostwald/tmp/ccs-nov-dec.log'
    lf = LogFile(path)

    entries = filter (None, filter (lambda x:x.get_query_param('uuid'), lf.data))

    entries.sort(key = lambda x:x.get_query_param('uuid'))

    uuids = []
    my_id = None
    for entry in entries:
        id = entry.get_query_param('uuid')
        if my_id != id:
            uuids.append(id)
            my_id = id

    print 'unique UUIds (%d)' % len(uuids)
    for id in uuids:
        print '-',id

    
if __name__ == '__main__':
    # path = '/Users/ostwald/tmp/ccs-nov-dec.log'
    # lf = LogFile(path)
    make_tally()
    # LogFileTester()

    
