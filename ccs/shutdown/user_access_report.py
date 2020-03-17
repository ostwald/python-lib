"""
make a tabdelimited file listing the users who have used ccs in past year or so
"""

import os, re, sys
from UserDict import UserDict
from get_user_record import getUserRecord

class Reporter(UserDict):

    def __init__ (self):
        self.data = {}
        self.init_data()

    def init_data(self):
        path = "TALLY.txt"
        lines = open(path, 'r').read().split('\n')

        #punt header
        lines = lines[1:]

        for line in lines:
            splits = map (lambda x:x.strip(), line.split('\t'))
            self[splits[0]] = splits[1]
            # print splits[0], splits[1]
        return

    def make_tab_delimited(self):
        recs=[];add=recs.append

        attrs = ['userName', 'email', 'firstName', 'lastName', 'schoolName', 'lastAccess', 'orgName']

        # header
        add (attrs)

        for i, key in enumerate(self.keys()):
            if i > 0 and i % 10 == 0:
                print '%d/%d' % ( i, len(self.keys()))
            rec = getUserRecord (key)
            rec.lastAccess = self[key]

            rec_data = []
            for attr in attrs:
                rec_data.append(str(getattr(rec, attr)))
            add (rec_data)

        print 'joining %d records' % len(recs)

        return '\n'.join(map (lambda x:'\t'.join(x), recs))

    def write_tab_delimited (self):
        outpath = "USER_ACCESS_REPORT.txt"
        fp = open(outpath, 'w')
        fp.write (self.make_tab_delimited())
        fp.close()
        print 'wrote to ',outpath

if __name__ == '__main__':
    rep = Reporter()
    # print rep.make_tab_delimited()
    rep.write_tab_delimited()