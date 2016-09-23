"""
abstract class for processing sources of citation data

- reads data from an (abstract) citation source,
- creates a 'Citation' record from each data record, and
- writes the records to a specified destination directory
"""

import os, sys
from citation import Citation

class GenericProcessor:
	"""
	abstract citation data processor to be instantiated for specific data
	sources, such as WOS or PUBs DB
	
	 - records - holds the raw data obtained from pubs
	"""
	destDir = None
	id_prefix = None
	records = []
	default_limit = 100000
	
	def __init__ (self, startid=None, limit=None, write=1):
		"""
		initialize self.destDir - the directory to which citation records will be written
		startid - first id to be assigned (defaults to the number of records currently in self.destDir
		
		concrete instances will populate self.records
		"""
		self.limit = limit or self.default_limit
		self.write = write
		if self.write and self.destDir is None:
			raise Exception, "write is set, but no destination is defined"
		
		if self.write and not os.path.exists (self.destDir):
				os.mkdir (self.destDir)
			
		if self.id_prefix is None:
			raise Exception, "id_prefix is not defined"

		# self.idcounter = startid or len (os.listdir (self.destDir)) + 1
		self.idcounter = self._idcounter_initial_value (startid)
		self.reccounter = 0
		
	def processRecords (self):
		"""
		transform records into data dictionaries, which are then transformed
		into Citation instances
		"""
		for rec in self.records:
			data = self.makeDataDict (rec)
			
			citation = Citation (data, self.makeId(self.idcounter))
			if self.write:
				citation.write (os.path.join (self.destDir, citation.id+'.xml'))
			else:
				print citation
			# print citation
			self.idcounter = self.idcounter + 1
			self.reccounter = self.reccounter + 1
			if self.reccounter >= self.limit: break
	
	def _idcounter_initial_value (self, startid):
		if startid:
			return startid
		if os.path.exists (self.destDir):
			return len (os.listdir (self.destDir)) + 1
		return 1
	
	def makeDataDict (self, rec):
		"""
		must be overridden by subclasses!
		
		returns a dictionary of field/values, where the fields must include items of
		'citation.required_fields'
		"""
		raise Exception, "makeDataDict not defined!"
				
	def makeId (self, idNum):
		thousands = idNum / 1000
		ones = idNum % 1000
		return "%s-000-000-%03d-%03d" % (self.id_prefix, thousands, ones)

