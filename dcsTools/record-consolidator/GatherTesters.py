"""
methods to peform checks on the GatherRecords process
"""
import os
from GatherRecords import Gatherer, gatherDir

## -------------- utils and debugging --------------------
		
def displayPrefixMap ():
	g = Gatherer(gatherDir)
	m = g.prefixMap
	print "prefixes"
	for key in m.keys():
		print "\t" + key + ": " + m[key]
		
def displayCollectionsByInstance():
	g = Gatherer(gatherDir)
	print "\n Collections by Instance"
	for instance in g.instances:
		print "\t", instance.name
		for collection in instance.collections:
			print "\t\t%s" % collection

def displayCollectionsByAlpha():
	g = Gatherer(gatherDir)
	print "\nAll Collections"
	allCollections = []
	for instance in g.instances:
		map (allCollections.append, instance.collections)
	allCollections.sort (lambda x,y: cmp(x.getShortTitle().lower(), y.getShortTitle().lower()))
	for collection in allCollections:
		print "\t%s" % collection

def matchConfigsWithPrefixMap ():
	g = Gatherer(gatherDir)
	configs = []
	print "config files"
	for i in g.instances:
		configs += map (lambda p: os.path.split (p)[1], i.collectionConfigs)
	if 0: # match prefixes to collection configs
		for c in configs:
			key, ext = os.path.splitext (c)
			try:
				prefix = g.prefixMap[key]
			except KeyError:
				prefix = "UNKNOWN"
			print "\t%s: %s" % (key, prefix)
	if 1: # match prefixes to configs
		cMap = {}
		for c in configs:
			key, ext = os.path.splitext (c)
			cMap[key] = c
		for key in g.prefixMap.keys():
			try:
				config = cMap[key]
			except KeyError:
				config = "MISSING"
			print "\t%s (%s): %s" % (key, g.prefixMap[key], config)

if __name__ == "__main__":
	matchConfigsWithPrefixMap()
