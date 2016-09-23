"""

Simulate the appearance of a new daily log file (e.g.,
'harvest.nsdl.org_access_log') in the working log file directory
('/home/ostwald/logs/log_files').

the individual logfiles are created by "log_splitter" and are named
with a suffix indicating their day order. This module moves the
LeastRecent ("oldest") log file (the one with the smallest index number) into the
working log directory and renames it as "harvest.nsdl.org_access_log"
"""


import os, sys, re
from UserDict import UserDict

class LogFileMover(UserDict):

    harvest_logs = '/home/ostwald/logs/harvest_logs'
    
    def __init__ (self):
        self.data = os.listdir(self.harvest_logs)
        self.data.sort(self.cmp)

    def cmp (self, one, other):
        get_val = lambda x:int(x.split('.')[-1])
        return cmp(get_val(one), get_val(other))

    def moveLeastRecent(self):

        top = self.data[0]

        # print top

        # print '.'.join(top.split('.'))[:-1]

        src = os.path.join (self.harvest_logs, top)
        dst = os.path.join ('/home/ostwald/logs/log_files',  os.path.splitext(top)[0])

        print 'src: %s\ndst: %s' % (src, dst)

        os.rename(src, dst)
        print 'moved', top

    def report (self):
        for file in self:
            print file

if __name__ == '__main__':
    mover = LogFileMover()
    mover.moveLeastRecent()
