"""
get_standards_hierarchical - this call returns json, which is converted into
a tree of StdNode objects.

TO DETERMINE:
- what is the hierarchy that is returned?? (are the leaf nodes what is really important?)
- are the roles of the input params? in particular, what role do the lexicon values play?
"""

import sys, os
import demjson
from urllib import urlopen, urlencode
from std import StdNode

baseurl = 'http://standards.teachersdomain.org/td_standards_json/get_standards_hierarchical/'

params = {
	'jurisdictions' : 'NY',
	'lexicon_terms' : '121,122',
	'grade_range' : 'k-12'
	}

data = urlopen (baseurl, urlencode(params))
"""
Returns a JSON formatted ordered 'node set' for a given Jurisdiction, list of Lexicon Term IDs and grade range
      use example: get_standards_hierarchical_json('NY','121,122','k-12')
"""


print "foo"
json = demjson.decode (data.read())
# print json
for tree in json:
	jurisdiction = tree[0]
	node = StdNode (tree[1])
	node.report()
