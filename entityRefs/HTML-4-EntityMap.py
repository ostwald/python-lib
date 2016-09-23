import string
import sys
import os

def makeMap ():
	map = {}
	s = open ('HTML-4-entities.txt', 'r').read()
	lines = s.split ("\n")
	print "%d lines read" % len(lines)
	i = 0
	for line in lines:
		linestart = "<!ENTITY "
		if len(line) == 0 or line[0:len(linestart)] != linestart: continue
		
		i = i + 1
	print "%d entities read" % i
	return map

def printMap (map):
	for key in map.keys():
		print 'charEntityMap.put ("%s", "%s");' % (key, map[key])

if __name__ == "__main__":
	map = makeMap ()
	print "map defines %d entities" % len(map)
