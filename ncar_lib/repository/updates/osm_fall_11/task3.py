"""
TASK 3. Update /record/resources/relation/@type = "Is published" , "Is referenced
by", "Is related", "Is replaced by", "References", "Unknown" records: 

a. For each entry, delete the contents of /record/resources/relation/@type and
remove the attribute because it is optional.
"""

from JloXml import XmlUtils
from updater import OsmCollectionUpdater, OsmUpdater

verbose = 1

relationTypesToRemove = ['Is published' , 'Is referenced by', 'Is related', 'Is replaced by', 
		 'References', 'Unknown']

def predicate (osmRecord):
	"""
	if there are any relations we might as well look...
	"""
	
	if verbose > 1:
		print '... task3 predicate'
	
	relations = osmRecord.selectNodes (osmRecord.dom, 'record/resources/relation')
	
	for relation in relations:
		if relation.hasAttribute ("type"):
			relType = relation.getAttribute ("type")
			if relType in relationTypesToRemove:
				return True
	
	# if len(relations) > 0:
		# return True
	return False
	
def action (osmRecord):
	"""
	
	For each entry, delete the contents of /record/resources/relation/@type and
	remove the attribute because it is optional.
	"""
	modified = False
	relations = osmRecord.selectNodes (osmRecord.dom, 'record/resources/relation')
	
	if verbose:
		print '\n-- task 3 action ---'
		if verbose > 1:
			print "%d relations found" % len(relations)
	
	for relation in relations:
		if relation.hasAttribute ("type"):
			relType = relation.getAttribute ("type")
			if relType in relationTypesToRemove:
				if verbose > 1:
					print "\n", relation.toxml()
				relation.removeAttribute("type")
				modified = True
		if verbose > 1:		
			print "\n", relation.toxml()

	# print osmRecord
	return modified
	
if __name__ == '__main__':

	# collection = 'my-osm'
	# osmPath = '/Users/ostwald/devel/dcs-repos/tiny/records/osm/'
	# format = OsmUpdater(osmPath)
	# collection = format.getCollection (collection)
	# collection.scan (predicate, action)
	pass
