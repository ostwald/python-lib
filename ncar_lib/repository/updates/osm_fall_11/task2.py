"""
TASK 2. see docs for predicate and actino
"""
import os, sys
from updater import OsmCollectionUpdater, OsmUpdater
from JloXml import XmlUtils

verbose = 1

def predicate (osmRecord):
	"""
	this task will fire for all records having
	/record/resources/relation/@type = 'Has image'
	"""
	# osmRecord.xpath_delimiter='/'
	
	if verbose > 1:
		print '... task2 predicate'
	
	relations = osmRecord.selectNodes (osmRecord.dom, 'record/resources/relation')
	for relation in relations:
		if relation.getAttribute ("type") == 'Has image':
			# print "      Has image relation FOUND"
			return True


	return False
	
def action (osmRecord):
	"""
	
	For each entry, move the contents of 
		/record/resources/relation/@title and @description to a new
	/record/general/description element
		
	The description content should have the title content, then a colon followed
	by description content. If there is only description content and no title
	content, skip the title content and colon.
	
	e.g., 
		<description>f:this is great</description>

	
	then DELETE the original relation
	
	"""
	
	
	if verbose > 1:
		print '%s HAS IMAGE: %s' % (getModuleName(), osmRecord.getId())
		
	# print osmRecord.__class__.__name__
	# if not osmRecord.getId():
		# print osmRecord
	modified = False
	
	relations = osmRecord.selectNodes (osmRecord.dom, 'record/resources/relation')
	if verbose:
		print '\n-- task 2 action fired ---'
		if verbose > 1:
			print "%d relations found" % len(relations)
	
	for relation in relations:
		if relation.getAttribute ("type") == 'Has image':
			title = ''
			if relation.hasAttribute ('title'):
				title = relation.getAttribute ("title")
				
			description = ''
			if relation.hasAttribute('description'):
				description = relation.getAttribute ("description")
				
			if verbose > 1:
				print 'title: "%s"' % title
				print 'description: "%s"' % description
				
			if title or description:
				msg = ''
				if title and description:
					msg = title + ':' + description
				else:
					msg = title + description
					
				description = osmRecord.addGeneralChild('description')
				XmlUtils.setText(description, msg)
			
			if verbose > 1:
				print 'WOULD HAVE DELETED RELATION'
				print "\n", relation.toxml()
				
			## delete the 'Has image' relation
			osmRecord.deleteElement(relation)
			modified = True
				
	return modified

	# print osmRecord

def getModuleName ():
	moduleName = None
	try:
		moduleName = name
	except NameError: 
		moduleName = os.path.basename(__file__)
	return moduleName
	
def getModuleAsTaskList ():
		
	from ncar_lib.repository.updates import TaskData, Task
	
	data = {
		'name':getModuleName(),
		'predicate':predicate,
		'action':action
	}
	task_data = TaskData (data)
	
	task = Task(task_data)
	print "getModuleAsTaskList(): %s" % task.name
	task.verbose = 0
	return [task]
	
def apply (path, printrec=None):
	rec = OsmRecord(path=path)
	if predicate(rec):
		action(rec)
		if printrec:
			print rec
	
def applyToFormat (baseFormatPath):
	"""
	used to be code under __main__ but seems to spin wheels
	"""
	# from updater import OsmUpdater
	
	
	print "Applying to Format: %s" % baseFormatPath
	format = OsmUpdater(baseFormatPath, getModuleAsTaskList())
	format.update()
	
def applyToCollection (collectionPath):
	# from updater import OsmCollectionUpdater
	format = 'osm'
	collection = OsmCollectionUpdater (collectionPath, format, getModuleAsTaskList())
	collection.update ()
	
	
def applyTester ():
	import os, sys
	from ncar_lib.osm import OsmRecord
	
	collection = '_test'
	osmPath = '/home/ostwald/tmp/osm-update-testing'
	filename = 'task_2.xml'
	path = os.path.join (osmPath, collection, filename)
	apply(path)
	
if __name__ == '__main__':
	
	from ncar_lib.osm import OsmRecord
	
	collection = '_test'
	osmPath = '/home/ostwald/tmp/osm-update-testing'
	path = os.path.join (osmPath, collection)
	
	path = 'test-recs/TEST-000-000-000-001.xml'
	apply (path, 1)

	# applyTester()
	# applyToCollection(path)
	# applyToFormat (osmPath)

	
