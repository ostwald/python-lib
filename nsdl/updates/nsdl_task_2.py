"""
Task 2 - 

/record/lifecycle/contributor/@role = Publisher AND 
/record/lifecycle/contributor == National Middle School Association (NMSA)
 
 -> Association for Middle Level Education (AMLE)
 
1274 total records
 
xmlFormat
- msp2
- math_path
collection
- 1235694767688
- 1252618532268
- 1316619387607
- 1250197406159

"""
import os, sys, re
from nsdl.formats import Msp2Record
from JloXml import XmlUtils

verbose = 1

task_name = 'nsdl_task_2'

find_str = 'National Middle School Association (NMSA)'
replace_str = 'Association for Middle Level Education (AMLE)'


def predicate (itemRecord):
	"""
	does this record have a relation of type 'Has image'?
	"""
	
	if verbose > 1:
		print '... %s predicate - %s' % (task_name, itemRecord.getId())
	
	producers = itemRecord.getPublishers()
	if verbose > 1:
		print "%d producers found" % len (producers)
		for p in producers:
			print '- %s' % p
		
	if find_str in itemRecord.getPublishers():
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
	
	for contrib in itemRecord.getContributorElements('Publisher'):
		if XmlUtils.getText (contrib) == find_str:
			XmlUtils.setText(contrib, replace_str)
		
if __name__ == '__main__':
	# repoPath = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo'
	# format = 'msp2'
	# collection = '1235694767688'
	# id = 'MSP2T-000-000-000-073'
	# path = os.path.join (repoPath, format, collection, id+'.xml')
	
	num = 1
	basePath = 'testers/task-2-tester-'
	if len(sys.argv) > 1:
		num = sys.argv[1]
	print 'NUM: %s' % num
	path = '%s%d.xml' % (basePath, int(num))
	
	rec = Msp2Record (path)
	if predicate(rec):
		action(rec)
	print rec
