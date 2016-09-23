"""
Task 5 - 
for records that have a license url of:
	beyondpenguins.nsdl.org ...
	
/key//record/rights/license/url:"http://beyondpenguins.nsdl.org/information.php?topic=use"
	
there were only 7 of these

this task has been executed!

	
"""
import os, sys, re
from nsdl.formats import NcsItemRecord
from JloXml import XmlUtils

verbose = 1

task_name = 'nsdl_task_5'

find_str = "http://beyondpenguins.nsdl.org/information.php?topic=use"
replace_str = 'http://beyondpenguins.ehe.osu.edu/terms-of-use'

def predicate (itemRecord):
	"""
	does this record have a relation of type 'Has image'?
	"""
	
	if verbose > 1:
		print '... %s predicate - %s' % (task_name, itemRecord.getId())
	
	licenseUrlValues = itemRecord.getLicenseUrlValues()
		
	for p in licenseUrlValues:
		if verbose > 1:
			print '- %s' % p
		if p.find (find_str) != -1:
			return True
	return False
	
def action (itemRecord):
	"""
	replace	terms of use urls
	"""

	if verbose:
		print "-- %s action --" % task_name
	
	rec_changed = False
	for licenseUrlEl in itemRecord.getLicenseUrlNodes():
		val = XmlUtils.getText (licenseUrlEl)
		if val.find(find_str) != find_str:
			XmlUtils.setText(licenseUrlEl, val.replace(find_str, replace_str))
			rec_changed = True
			
if __name__ == '__main__':
	if 0:
		num = 1
		basePath = 'testers/task-5-tester-'
		if len(sys.argv) > 1:
			num = sys.argv[1]
		print 'NUM: %s' % num
		path = '%s%d.xml' % (basePath, int(num))
	
	changed = 0
	basedir = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo/ncs_item/1239144881424'
	for filename in os.listdir (basedir):
		path = os.path.join (basedir, filename)
		rec = NcsItemRecord (path)
		if predicate(rec):
			# action(rec)
			# print rec
			# sys.exit()
			changed += 1
			
	print "%d changed records" % changed

