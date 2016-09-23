import string
import sys
import os

"""
parses a file containing mappings from character to numeric references, and
produces javacode for populating a Map structure with the mappings.

produces mappings for all entities defined in HTML-4 spec
"""

def makeMap ():
	s = open ('entities.txt', 'r').read()

	map = {}

	lines = s.split ("\n")
	print "%d lines read" % len(lines)
	i = 0
	for line in lines:
		if len(line) == 0 or line[0] != '&': continue

		splits = line.split("\t")
		if len(splits) < 3:
			print line
			continue

		map[splits[0]] = splits[2]
		i = i + 1
	print "%d references found" % i
	return map

def printMap (map):
	"""
	prints java code that will populate a Map named "charEntityMap" with
	mappings from character to numeric entity refs

	output to be cut and pasted into java class
	"""
	for key in map.keys():
		print 'charEntityMap.put ("%s", "%s");' % (key, map[key])

if __name__ == "__main__":
	map = makeMap()
	print "map defines %d entities" % len(map)
	printMap (map)
