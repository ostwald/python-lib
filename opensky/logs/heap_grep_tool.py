"""
the log files are very large and we want to get a feel for where/when the out of memory errors
are occcuring.

as first stab, we analysze a grep out put file created by command:

grep -n heap catalina.out-3_25-4_2 > heap_3_25-4_2.txt

"""
import sys, re
from UserDict import UserDict

path = 'heap_3_25-4_2.txt'

lines = filter (None, map (lambda x:x.strip(), open(path, 'r').read().split('\n')))

data = {}

last = 0
for i, line in enumerate(lines):
    # print '- %s' % line.split(':')[0]
    linenum = int(line.split(':')[0])
    delta = linenum - last
    last = linenum

    entry = data.has_key(delta) and data[delta] or []
    entry.append (linenum)
    data[delta] = entry

keys = data.keys()
keys.sort()
for key in keys:
    print '%s: %s' % (key, data[key])