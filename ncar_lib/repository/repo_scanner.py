import sys, os
from xml_dec_repair import DeclarationFixer
from ncar_lib.osm import OsmRecord


def recordReport (rec, indent):
	print indent + "%s" % rec.getId()

OsmRecord.report = recordReport
	
## --- SET-Up - define action functions that will get called for the appropriate scanners
		
def showCollectionName (collectionScanner):
	print 'scanning collection: %s' % collectionScanner.name

def recordAction (caller, osmRecord):
	print "RECORD_ACTION %s" % osmRecord.getId()

class Record:
	
	def __init__ (self, path, parent=None):
		self.path = path
		self.name = os.path.basename(path)
		self.parent = parent
		self.fixer = DeclarationFixer (self.path)
		
	def __repr__ (self):
		return self.name
		
	def getFormat (self):
		return self.parent.getFormat()
		
	def getCollection (self):
		return self.parent.name
		
	def report (self, indent=""):
		print indent + "%s" % self.name
		# print indent + "%s (%s)" % (self.name, self.getFormat())
		# print indent + "%s (%s)" % (self.name, self.getCollection())

class DirectoryScanner:
	"""
	abstract class to 
	- visit all items in a directory
	- instantiate an 'item_class' instance for each
	"""
	item_name = 'XXX'
	item_class = None
	my_action = None
	
	def __init__ (self, path, parent=None):
		self.path = path
		self.name = os.path.basename(path)
		self.parent = parent
		# print "processing %s" % self.name
		self.items = self.get_items()
		if self.my_action:
			self.my_action()
		
	def get_items(self):
		items=[];add=items.append
		for filename in os.listdir(self.path):
			path = os.path.join(self.path, filename)
			if self.accept_item (path):
				# instantiate ITEM_CLASS
				add (self.createItem (path))
		return items

	def createItem (self, path):
		return self.item_class (path, parent=self)
		
	def accept_item (self, path):
		return 1
		
	def __repr__ (self):
		return self.name
		
	def report (self, indent=""):
		print indent + "%s report" % self.__class__.__name__
		print indent + "  name: %s" % self.name
		print indent + "  path: %s" % self.path
		print indent + "  %ss:" % self.item_name
		for item in self.items:
			# print indent + '     %s' % item
			item.report (indent + "\t")
			
	def mapApplyToItems (self, item_fn):
		map (item_fn, self.items)
			
class CollectionScanner (DirectoryScanner):
	
	item_name = "record"
	item_class = OsmRecord
	record_action = recordAction
	my_action = showCollectionName
	
	def __init__ (self, path, parent=None):
		DirectoryScanner.__init__(self, path, parent)

		if self.record_action:
			map (self.record_action, self.items)
	
	def getFormat (self):
		return self.parent.name
	
	def accept_item (self, path):
		if os.path.isdir (path): return 0
		name = os.path.basename (path)
		if name[0] == '.': return 0
		if not name.endswith ('.xml'): return 0
		return 1
		
	def createItem (self, path):
		return self.item_class (path)
			
class FormatScanner (DirectoryScanner):
	
	item_name = "collections"
	item_class = CollectionScanner
		
	def accept_item (self, path):
		if not os.path.isdir (path): return 0
		name = os.path.basename (path)
		if name[0] == '.': return 0
		return 1
		
class RepositoryScanner (DirectoryScanner):
	
	item_name = "format"
	item_class = FormatScanner
		
	def accept_item (self, path):
		if not os.path.isdir (path): return 0
		name = os.path.basename (path)
		if name[0] == '.': return 0
		if name == 'dcs_data': return 0
		return 1
		
	
## - assign action functions to variables known to the scanners
	
repo_base = '/Users/ostwald/devel/python-lib/ncar_lib/repository/updates/6_23_fiscalYear_Rights/records'

def repositoryScannerTester ():
	path = repo_base
	scanner = RepositoryScanner(path)
	# scanner.report()
	
def formatScannerTester ():
	path = '/devel/ostwald/records/ncs-records/ncs_item'
	path = os.path.join (repo_base, 'osm')
	FormatScanner(path)
	
def collectionScannerTester ():
	# path = '/devel/ostwald/records/ncs-records/ncs_item/1193182292279'
	path = os.path.join (repo_base, 'osm/jkuettner')
	CollectionScanner(path)
	
if __name__ == '__main__':
	# repositoryScannerTester()
	# formatScannerTester()
	collectionScannerTester()
