"""
Task 1 -  NMSA Collection (plus others see below)

in URLs, nmsa -> amle (check to make sure new urls are going to work)
nmsa.org -> www.amle.org
 
1211 total records 
 
xmlFormat
- msp2
- math_path
collection
- 1235694767688
- 1252618532268
- 1316619387607
- 1250197406159

TASK Completed

"""
import os, sys, re
from nsdl.formats import Msp2Record
from JloXml import XmlUtils

verbose = 1

task_name = 'nsdl_task_1'

find_str_1 = 'http://www.nmsa.org'
find_str_2 = 'http://nmsa.org'

find_pat = re.compile ("http://(.*)\.org")

# replace_str = 'http://www.amle.org'
replace_str = 'www.amle'


def predicate (itemRecord):
	"""
	does this record have a relation of type 'Has image'?
	"""
	
	if verbose > 1:
		print '... %s predicate - %s' % (task_name, itemRecord.getId())
	
	url = itemRecord.getUrl()
	if url.find(find_str_1) != -1 or url.find(find_str_2) != -1:
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
		print '\n-- nsdl_task_1 action ---'
		before = url = itemRecord.getUrl()
		
		m = find_pat.match (url)
		url = url.replace (m.group(1), replace_str)
		if verbose > 1:
			print 'url before: %s' % before
			print 'url after: %s' % url
		itemRecord.set ('url', url)
		
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
