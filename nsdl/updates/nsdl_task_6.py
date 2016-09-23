"""
Task 6 ALT - 
THIS IS A STANDALONE TASK ...

there are many isPartOf urls that contain "http://beyondpenguins.nsdl.org"

e.g., http://beyondpenguins.nsdl.org/issue/index.php?date=April2009

<record>
    <relations>
        <isPartOf>
            <url>
                http://beyondpenguins.nsdl.org/issue/index.php?date=April2009


there are 47 unique values, 206 instance in all.

use the mappings table from the nsdl.org transition and find the mapped urls.

This Task has executed!

"""

import os, sys, re
from nsdl.formats import Msp2Record
from JloXml import XmlUtils

verbose = 1

task_name = 'nsdl_task_6_ALT'

def getUniqueValues ():
	
	colDir = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo/ncs_item/1239144881424/'
	for filename in os.listdir(colDir):
		path = os.path.join (colDir, filename)
		rec = NcsItemRecord(path=path)
		for node in rec.getIsPartOfUrlNodes():
			value = XmlUtils.getText(node)
			if not value in unique_values:
				# print value
				unique_values.append(value)
				
	return unique_values
	
if __name__ == '__main__':
	from bppb_rules import BPPBMappings
	from nsdl.formats import NcsItemRecord
	mappings = BPPBMappings()
	print 'table has %d entries' % len(mappings)
	
	unique_values = []
	
	colDir = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo/ncs_item/1239144881424/'
	for filename in os.listdir(colDir):
		path = os.path.join (colDir, filename)
		rec = NcsItemRecord(path=path)
		rec_changed = False
		for node in rec.getIsPartOfUrlNodes():
			value = XmlUtils.getText(node)
			mapping = mappings.getMapping(value)
			if mapping is None:
				print "NO mapping", value
			else:
				print "MAPPING", mapping
				XmlUtils.setText(node, mapping)
				rec_changed = True
		if rec_changed:
			# print 'WOULD HAVE WRITTEN', rec.getId()
			rec.write()
			

