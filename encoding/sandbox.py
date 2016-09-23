# coding=utf-8
import sys

a = '“'
h = '“hello”'
i = u'hello\u0020world'

def showStuff (s):
	print "\n-------------"
	print "input:", s

	print type (s)
	print 'length: %d' % len (s)

	for ch in s:
		print ch, ord(ch)

for yo in [a,h,i]:
	showStuff (yo)
showStuff (i)
