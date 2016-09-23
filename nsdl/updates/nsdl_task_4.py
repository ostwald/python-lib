"""
Task 4 - 
THIS IS A STANDALONE TASK ...

BPPB collection fix URLS. 

See nsdl.org redirects, e.g., beyondpenguins.nsdl.org -> xxxxx

"""
import os, sys, re
from nsdl.formats import Msp2Record, NcsItemRecord
from JloXml import XmlUtils

from bppb_rules import BPPBMappings

verbose = 1

task_name = 'nsdl_task_4'

		
def updateCollection (colDir):
	"""
	mappings table contains old and new url mappings which are applied
	to the collection's url field.
	"""
	mappings = BPPBMappings()
	print 'table has %d entries' % len(mappings)
	
	# vist each item record
	for filename in os.listdir(colDir):
		path = os.path.join (colDir, filename)
		rec = NcsItemRecord(path=path)
		url = rec.getUrl()
		if mappings.has_key(url):
			newUrl = mappings[url]
			rec.setUrl (newUrl)
			rec.write()
		else:
			if url.find('beyondpenguins.nsdl.org') != -1:
				print "no mapping for", url
	
if __name__ == '__main__':

	print 'table has %d entries' % len(mappings)
	
	colDir = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo/ncs_item/1239144881424/'
	for filename in os.listdir(colDir):
		path = os.path.join (colDir, filename)
		rec = NcsItemRecord(path=path)
		url = rec.getUrl()
		if mappings.has_key(url):
			newUrl = mappings[url]
			rec.setUrl (newUrl)
			rec.write()
		else:
			if url.find('beyondpenguins.nsdl.org') != -1:
				print "no mapping for", url
