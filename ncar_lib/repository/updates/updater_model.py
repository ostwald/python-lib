"""

Repository Updater -

ObjectUpdater updates metadat records by runing a series of Tasks against each.

Updaters 
- Repository
-- Format
-- Collection
--- ObjectUpdater - item level

"""
import os, sys, re
from UserDict import UserDict
from UserList import UserList
from JloXml import MetaDataRecord

verbose = 1
dowrites = 0
prefixPat = re.compile ('(.*?)-000.*')

def getPrefix (recId):
	"""
	return prefix portion of provided record ID, e.g., DLESE-000-000-001
	"""
	m = prefixPat.match (recId)
	if not m:
		raise Exception, 'getPrefix: prefix not found (%s)' % recId
	return m.group(1)

class ObjectUpdater:
	"""
	instantiated once, and then called repeatedly witih objects to operate upon
	"""
	
	def __init__ (self, tasks):
		self.tasks = tasks
		
	def update (self, object):
		if verbose > 1:
			print '\n-----------------------------'
			print 'updating Item', object.getId()
			
		# print ' object type: %s' % object.__class__.__name__
		# rint '     %d tasks' % len (self.tasks)
		
		object_modified = False
		for task in self.tasks:
			
			if task.predicate (object):
				try:
					modified = task.action (object)
					if modified:
						object_modified = True
					if verbose > 1:
						print '-task: %s (%s)' % (task.name, modified)
					if not modified in (True, False):
						raise Exception, 'Task (%s) action did not return True or False' % task.name
				except Exception, e:
					print 'could not process %s: %s' % (object.getId(), e)
					raise e
						
		if object_modified:
			if dowrites:
				object.write()
				if verbose:
					print 'wrote: ', object.getId()
			else:
				if verbose:
					# print "would have written", object.getId()
					print 'would have written %s (%s)' % (object.getId(), os.path.basename(object.path))
			
				
class Collection (UserList):
	"""
	items are instances of itemClass, accessed via list API
	"""
	level = 'collection'
	itemClass = MetaDataRecord
	
	def __init__ (self, baseDir, format, tasks):
		self.data = None
		self.format = format   # e.g., osm
		self.baseDir = baseDir
		self.tasks = tasks
		self.key = os.path.basename(self.baseDir)
		
	def accept (self, path):
		"""
		do we instantiate item at this path?
		"""
		name = os.path.basename (path)
		if name[0] in ['.']:
			return 0
		if name[-1] in ['~']:
			return 0
		if not name.endswith('.xml'):
			return 0
		# if len(self) > 10:
			# return 0
		return 1
		
	def update (self):
		print '\n-----------------------------'
		print 'updating Collection: %s (%s)' % (self.key, self.format)
		if False and verbose:
			mytasks = self.tasks
			if mytasks:
				if not type(self.tasks) == type([]):
					mytasks = [mytasks]
					
				for task in mytasks:
					print "task class: ", task.__class__.__name__
					print "task.name: ", task.name
					
					
				print "tasks: %s" % ', '.join(map (lambda x:x.name, mytasks))
			else:
				print "no tasks defined"
				
		objectUpdater = ObjectUpdater (self.tasks)
		
		if self.data == None:
			self.read (objectUpdater)
			
		else:
			for item in self:
				objectUpdater.update(item)
		
	def read (self, objectUpdater=None):
		"""
		populate user.data from file system
		"""
		if self.data == None:
			print "%s ..." % (objectUpdater and "updating" or "reading")
			self.data = []
			recFiles = os.listdir(self.baseDir)
			numRecs = len(recFiles)
			for i, recFile in enumerate(recFiles):
				path = os.path.join (self.baseDir, recFile)
				if self.accept (path):
					rec = self.instantiateItemClass (path=path)

					self.append(rec)
					# self.append (self.itemClass (path=path)) # we assume itemClass is an XmlRecord
				
					if objectUpdater:
						objectUpdater.update(rec)
						
				if verbose and i and i % 500 == 0:
					print '%d/%d' % (i, numRecs)
					
			print '... processed %d items' % len(self)
					
	def instantiateItemClass (self, path):
		try:
			self.itemClass.xpath_delimiter = '/'
			instance = self.itemClass(path=path)
			
			return instance
			# return self.itemClass(path=path)
		
		except UnicodeDecodeError, err:
			print "could not read file at %s" % path
			raise err
				
	def scan (self, pred, action):
		"""
		pred and action are functions that take: object (instance of itemClass), context={whatever}
		
		for each item,
		- appy pred
		- if pred, then apply action
		"""
		
		for item in self:
			if pred (item): action (item)
		
class Format (UserDict):
	"""
	items are collections, dict API to collections (key are collectionKeys)
	"""
	
	level = 'format'
	itemClass = Collection
	
	def __init__ (self, baseDir, tasks):
		self.data = None
		self.baseDir = baseDir
		self.tasks = tasks
		self.format = os.path.basename(self.baseDir)
		
		
		
	def accept (self, path):
		name = os.path.basename(path)
		if name[0] == '.':
			return 0
		if name[-1] in ['~']:
			return 0
		if not os.path.isdir(path):
			return 0
		return 1
		
	def read (self):
		"""
		instantiates an 'itemClass' (e.g., Collection) for each directory
		
		will only read new data once, no matter how many times called
		"""
		if self.data is None:
			self.data = {}
			for colDir in os.listdir(self.baseDir):
				path = os.path.join (self.baseDir, colDir)
				if self.accept (path):
					try:
						# print 'Format about to instantiate item (%s)' % self.itemClass.__name__
						self[colDir] = self.instantiateItemClass (path, self.format, self.tasks)
					except IOError , e:
						msg = "Format %s: Failed to instantiate itemClass: %s" % \
								(self.format, self.itemClass.__name__)
						print msg
						raise e
				
	def instantiateItemClass (self, path, format, tasks):
		"""
		hook for customizing instantiation of collection classes. Could be used
		if different readers were used for different collections
		"""
		return self.itemClass(path, format, tasks)
		
	def update (self):
		"""
		call 'update' method on each collection
		"""
		for collection in self.getCollections():
			collection.update()
		
	def getCollectionKeys (self):
		self.read()
		return self.keys()
		
	def getCollections (self):
		"""
		get instances of self.itemClass
		"""
		self.read()
		return self.values()
	
	def getCollection (self, key):
		"""
		get collection for provided key
		"""
		self.read()
		try:
			return self[key]
		except KeyError:
			print 'no such collection: %s' % key
			return None
			
class Repository (UserDict):
	"""
	items are collections, dict API to collections (key are collectionKeys)
	"""
	
	level = 'repository'
	itemClass = Format
	
	def __init__ (self, baseDir, tasks):
		self.data = None
		self.baseDir = baseDir
		self.tasks = tasks
		
	def accept (self, path):
		name = os.path.basename(path)
		return name[0] != '.' and name[-1] not in ['~']
		
	def read (self):
		if self.data is None:
			self.data = {}
			for formatDir in os.listdir(self.baseDir):
				path = os.path.join (self.baseDir, formatDir)
				if self.accept (path):
					try:
						print 'Repo about to instantiate item (%s)' % self.itemClass.__name__
						self[formatDir] = self.instantiateItemClass (path, self.tasks)
					except IOError , e:
						msg = "Repo %s: Failed to instantiate itemClass: %s" % \
								(self.format, self.itemClass.__name__)
						print msg
						raise e
				
	def instantiateItemClass (self, path, tasks):
		return self.itemClass(path, tasks)
		
	def update (self):
		for format in self.getFormats():
			format.update()
		
	def getFormatKeys (self):
		self.read()
		return self.keys()
		
	def getFormats (self):
		self.read()
		return self.values()
	
	def getFormat (self, key):
		self.read()
		try:
			return self[key]
		except KeyError:
			print 'no such format: %s' % key
			return None
	
class TaskData:
	"""
	data that dan be sent to Task to approximate a module, which is 
	what Task exects
	"""
	def __init__ (self, data=None):
		self.name = self.predicate = self.action = None
		if data:
			
			self.name = data.has_key('name') and data['name'] or "name unknown"
			self.__name__ = self.name
			self.predicate = data['predicate']
			self.action = data['action']
			
			print data
class Task:
	
	def __init__ (self, taskModule):
		self.module = taskModule
		self.predicate = taskModule.predicate
		self.action = taskModule.action
		self.name = hasattr(taskModule, 'name') and taskModule.name or taskModule.__name__
		print 'initialized task', self.name
	
	def _predicate (self, object, context=None):
		"""
		determines whether the action of this Task will be invoked
		- by default selects all
		"""
		return 1
		
	def _action (self, object, context=None):
		"""
		task action operates on object
		"""
		print object.getId()
	
	def setVerbose (self, level):
		# print 'set verbose for %s to %s' % (self.name, level)
		try:
			self.module.verbose = level
		except Exception, e:
			print "could NOT set verbose: %s" % s
		
def _myPredicate (rec):
	"""
	selects objects to be acted upon
	"""
	return 1
			
def _myAction (rec):
	"""
	acts upon selected object
	"""
	print rec.getId()
			
def makeTask (name, action, predicate):
	return 
	
if __name__ == '__main__':
	pass
	
