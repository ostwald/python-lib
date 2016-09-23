"""
   quick script for analysing the crash log from startup to crash
"""

import string

## fileName = "Crash5-02012005/startup-2-crash.log"
## fileName = "Crash4-01272005/startup-2-crash.log"
fileName = "Crash3-01272005/startup-2-crash.log"

f = open(fileName, 'r')
s = f.read()
f.close()

lines = s.split('\n')

get_pattern = "INFO: Processing a 'GET' for path "
post_pattern = "INFO: Processing a 'POST' for path "

gets = []
posts = []
paths = []

for line in lines:
	if string.find (line, get_pattern) == 0:
		gets.append(line)
		paths.append ("GET: " + line[len(get_pattern):])
	elif string.find(line, post_pattern) == 0:
		posts.append(line)
		paths.append ("POST: " + line[len(post_pattern):])
		
print "there are %d lines" % len (lines)
print "there are %d GETS" % len (gets)
print "there are %d POSTS" % len (posts)

for path in paths:
	print path
