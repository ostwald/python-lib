"""
Task 3 - 
if a rights value has a value containing "National Middle School Association (NMSA)"
replace with "Association for Middle Level Education (AMLE)"

/record/lifecycle/contributor/rights
 
1273 total records
 
xmlFormat
- msp2
- math_path
collection
- 1235694767688 - msp2
- 1252618532268 - msp2
- 1316619387607
- 1250197406159

"""
import os, sys, re
from nsdl.formats import Msp2Record
from JloXml import XmlUtils

verbose = 1

task_name = 'nsdl_task_3'

find_str = 'National Middle School Association (NMSA)'
replace_str = 'Association for Middle Level Education (AMLE)'


def predicate (itemRecord):
	"""
	does this record have a relation of type 'Has image'?
	"""
	
	if verbose > 1:
		print '... %s predicate - %s' % (task_name, itemRecord.getId())
	
	rightsValues = itemRecord.getRightsValues()
	if verbose > 1:
		print "%d rightsValues found" % len (rightsValues)
	for p in rightsValues:
		if verbose > 1:
			print '- %s' % p
		if p.find (find_str) != -1:
			return True
	return False
	
def action (itemRecord):
	"""
	
	For each entry, move the contents of /record/resources/relation/@title and
	@description to a new /record/resource/description field. The description
	field should have the title content, then a colon followed by description
	content. If there is only description content and no title content, skip the
	title content and colon.
	"""

	if verbose:
		print "-- %s action --" % task_name
	
	for rightsEl in itemRecord.getRightsElements():
		val = XmlUtils.getText (rightsEl)
		if val.find(find_str) != find_str:
			XmlUtils.setText(rightsEl, val.replace(find_str, replace_str))
		
if __name__ == '__main__':
	# repoPath = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo'
	# format = 'msp2'
	# collection = '1235694767688'
	# id = 'MSP2T-000-000-000-073'
	# path = os.path.join (repoPath, format, collection, id+'.xml')
	
	num = 1
	basePath = 'testers/task-3-tester-'
	if len(sys.argv) > 1:
		num = sys.argv[1]
	print 'NUM: %s' % num
	path = '%s%d.xml' % (basePath, int(num))
	
	rec = Msp2Record (path)
	if predicate(rec):
		action(rec)
	print rec
