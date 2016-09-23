"""

update all osm records. this is done by invoking 'conditional actions' on each osmRecords

tasks are registered, and then called sequentially 

"""

import os, sys
from ncar_lib import OsmRecord
from ncar_lib.repository.updates import Repository, Format, Collection, ObjectUpdater, Task, dowrites

verbose = 1
dowrites = 0


def getTasks ():
	import task2, task3, task5, task6, task7, task9, task10, task11, task12, task13

	# itemTasks = map (Task, [task13])
	itemTasks = map (Task, [task2, task3, task5, task6, task7, task9, task10, task11, task12, task13])
	
	if verbose > 1:
		print '\ngetTasks()'
	for task in itemTasks:
		if verbose > 1:
			print '- ', task.name
		task.setVerbose (0)
	
	return itemTasks

class OsmCollectionUpdater (Collection):
	
	itemClass = OsmRecord
	
	def __init__ (self, baseDir, format=None, itemTasks=None):
		Collection.__init__ (self, baseDir, format, itemTasks)
	
class OsmUpdater (Format):

	itemClass = OsmCollectionUpdater
	
	# def __init_ (self, baseDir):
	
	def __init__ (self, baseDir, tasks):
		Format.__init__ (self, baseDir, tasks)

def updaterHelper ():
	# osmPath = '/Users/ostwald/devel/dcs-repos/tiny/records/osm/'
	
	osmPath = '/home/ostwald/tmp/osm-update-testing'

	level =  'format' # 'collection',  'format'
	
	formatUpdater = OsmUpdater(osmPath, getTasks())
	if level == 'format':	
		formatUpdater.update ()
		
	elif level == 'collection':
		#collection = "osgc"
		collection = "wwashington"
		collectionUpdater = formatUpdater.getCollection (collection)
		collectionUpdater.update ()	
		
if __name__ == '__main__':
	import task2, task3, task5, task6, task7, task9, task10, task11, task12, task13
	coll_path = 'test-recs'
	tasks = map (Task, [task2, task3, task5, task6, task7, task9, task10, task11, task12, task13])
	if 0: # one task at a time
		for task in tasks:
			print '+++++++++++++++++++++++++++++++++++'
			print task.name
			task.setVerbose (False)
			collectionUpdater = OsmCollectionUpdater (coll_path, 'osm', [task])	
			collectionUpdater.update()
	if 1:
		map (lambda t:t.setVerbose(0), tasks)
		collectionUpdater = OsmCollectionUpdater (coll_path, 'osm', tasks)
		collectionUpdater.update()
			
	
