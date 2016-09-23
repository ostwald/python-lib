"""
PRODUCTION as of 10/14/15

read individual csv files into a ginormus mapping from Ark to citableUrl

probably will need a recursive slopper to get all csv files under a particular folder

NOTE: DIL data has different form, so slurper can't accept dil mapping files

"""

import os, sys, re, time
from UserDict import UserDict
from tabdelimited import CsvFile, CsvRecord
from JloXml import XmlRecord, XmlUtils

host = os.environ['HOST']
config = {}
if host == 'purg.local':
	config['idRepoDir'] = '/Users/ostwald/devel/github/libroot/production/identifiers/'
	# config['targetFile'] = '/Users/ostwald/devel/projects/nldr-project/web/WEB-INF/data/arkMappings.xml'
else:
	config['idRepoDir'] = '/Users/ostwald/devel/git/libroot/production/identifiers/'

class ArkDataRecord (CsvRecord):
	"""
	first row, first cell has name of form: "# COLLECTION : archives:amsohp"
	whereas the first cell of the data records is the ark id
	
	UPDATE: we can't count on the header row contents, so just assign
	based on column position (which we can depend on)
	
	expose attributes:
	- ark, pid, osm
	"""

	def __init__ (self, data, parent):
		CsvRecord.__init__(self, data, parent)
		self.ark = self.getCellContents(0)
		self.pid = self.getCellContents(1)
		self.osm = self.getCellContents(2)
		
	def getCellContents(self, colNum):
		try:
			return self.data[colNum]
		except IndexError:
			return ''

class ArkDataTable (CsvFile):
	 linesep = '\n'
	 record_constructor = ArkDataRecord
	 
	 def __init__ (self, file):
	 	 CsvFile.__init__(self)
	 	 self.read(file)

class MappingRecord (XmlRecord):
	
	def __init__ (self):
		stub = '<arkMappings date="%s"></arkMappings>' % time.asctime()
		XmlRecord.__init__ (self, xml=stub)
		
	def addMapping (self, ark_id, osm_id):
		el = self.addElement(self.doc, 'mapping')
		el.setAttribute('arkId', ark_id)
		el.setAttribute('osmId', osm_id)
		
	def __len__ (self):
		return len(self.getElements(self.doc))
		
	def write (self, path):
		XmlRecord.write(self, path)
		print 'wrote to ', path

class Slurper:
	
	skip_files = ['OLD_dil_ezid_pid_production_map.csv','opensky_imagegallery.csv']
	max_files = sys.maxint
	
	def __init__ (self, root):
		self.root = root
		# self.mapping = UserDict()
		self.mappings = MappingRecord()
		self.skipped_recs = 0
		
	def accept(self, path):
		if path[0] in ['.']:
			return 0
		if os.path.isdir (path): return 0
		
		if os.path.basename(path) in self.skip_files:
			return 0
		
		return path.endswith('.csv')
		
	def slurp (self, base):
		
		paths = filter (self.accept, 
				        map(lambda x:os.path.join (base, x), os.listdir(base)))
		
		for i, path in enumerate(paths):
			if i >= self.max_files:
				break
				
			table = ArkDataTable (path)
			for record in table:
				# self.mapping[record['id']] = record['ark']
				if record.ark and record.osm:
					self.mappings.addMapping(record.ark, record.osm)
					if record.osm == 'OSGC-000-000-000-670':
						print ' added Mapping for OSGC-000-000-000-670'
				else:
					self.skipped_recs += 1
			print 'processed %s (%d)' % (os.path.basename(path), len(table))

def tableTester (filename):
	tester = os.path.join (config['idRepoDir'],filename)
	table = ArkDataTable (tester)
	print 'table has %d records' % len(table.data)

	for i, row in enumerate(table):
		print '%d - %s -> %s' % (i, row.ark, row.osm)

def doSlurp (target=None):
	target = target or (config.has_key('targetFile') and config['targetFile']) or "TEST_MAPPINGS.xml"
	slurper = Slurper (os.path.join (config['idRepoDir']))
	# slurper = Slurper (dataBase)
	slurper.slurp(slurper.root)
	print len(slurper.mappings), 'mappings'
	slurper.mappings.write(target)
	print 'skipped_recs: %d' % slurper.skipped_recs

if __name__ == '__main__':
	doSlurp()
	# tableTester ('research_dataviz.csv')
	
