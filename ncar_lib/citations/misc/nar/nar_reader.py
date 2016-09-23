"""
try to make sense of OCR results from NAR reports

notes - if we replace all funny chars in source with "-" (using jedit) the
we can read file as normal ASCII.
"""

import codecs
import re

def read1():

	# datafile = "NAR_1969_Publications.txt"
	datafile = "1969_frag.txt"

	fp = codecs.open (datafile, 'r', 'utf-8')
	u = fp.read()
	# s = open(datafile).read()
	# u = unicode (s, "utf-8")

	print u.encode ('utf-8', 'replace')[:1000]

def read2():

	# datafile = "NAR_1969_Publications.txt"
	datafile = "1969_frag.txt"

	s = open(datafile).read()
	return s

def splitItems (s):
	"""
	try to recognize the various versions of "_______" at the begining of
	a record
	"""
	delimeter = "\n\n***********"
	patStr = "(\n[-,.]+)"
	pat = re.compile (patStr, re.M)
	buff = ""
	i = 0
	while i < len(s):
		m = pat.match (s,  i)
		if m:
			# print "found (%s)" % m.group(1)
			buff = buff + delimeter
			i = i + len (m.group(1))
		else:
			# print "NOT found"
			buff = buff + s[i]
			i = i + 1
	return buff
	

foo = '\n,---.-------:and...'

data = read2()
# print data
print "\n---------\n%s\n-----------------\n" % splitItems(data)
