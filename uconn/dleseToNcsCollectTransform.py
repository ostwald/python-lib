import os, sys, time
from JloXml import DleseCollectRecord, XmlUtils
from nsdl.ncs.NcsCollectRecord import NCSCollectRecord


class DleseToNcsCollectTransform:
	
	ncs_collect_template = '/Users/ostwald/devel/python/python-lib/uconn/ncs_collect_template.xml'
	tmp_output_path = '/Users/ostwald/tmp/dlese_to_ncs_collect'
	
	"""
	field_mappings documentation
	"""
	field_mappings = [
		# dlese_collect -> ncs_collect
		'id', # we do id by hand
		'description',
		['collectionLocation', 'url'],
		['fullTitle' , 'title'],
		['id' , 'collSetSpec'],
		['created' ,'dateTime'], # involves a massage
		'libraryFormat',
		['key', 'oaiSetSpec']
	]
	
	def __init__ (self, dcr_path, id=None):
		self.initialized = False
		self.dcr = DleseCollectRecord (path=dcr_path)
		self.ncr = NCSCollectRecord(path=self.ncs_collect_template)

		self.process_field_mappings()
		self.injectContributors()
		xmlFormat = self.dcr.get('libraryFormat') 
		if (xmlFormat == 'adn'):
			self.ncr.addViewContext ('DLESECollections')
			self.ncr.set ('metadataPrefix', 'nsdl_dc')
		elif (xmlFormat == 'dlese_anno'):
			self.ncr.addViewContext ('DLESEAnnotations')
			self.ncr.set ('metadataPrefix', 'comm_anno')
			
		if id:
			self.ncr.setId(id)

		#set the destination (ncr) path for writing
		self.ncr.path = os.path.join (self.tmp_output_path, self.ncr.getId()+'.xml')
		self.initialized = True

	def injectField (self, dcr_field, ncr_field=None):
		if ncr_field is None:
			ncr_field = dcr_field
			
		# get value from dcr_field
		try:
			value = self.dcr.get(dcr_field)
			if not value:
				# msg = 'WARN: injectField - no value for "%s" in %s' % (dcr_field, self.dcr.getId())
				# print msg
				raise Exception, "no value in metadata"
		except Exception, msg:
			print "WARN ingest did NOT get value for %s at '%s': %s" % (self.dcr.getId(), dcr_field, msg)
			value = ""
			
		# kludges for certain fields
		if dcr_field == 'created':
			value += 'T00:00:00Z'
			
		if ncr_field == 'collSetSpec':
			value = 'ncs-' + value
			
		# inject value in ncr_field
		try:
			print 'setting "%s" at "%s"' % (value, ncr_field)
			self.ncr.set(ncr_field, value)
		except Exception, msg:
			print "ERROR setting value at '%s': %s" % (ncr_field, msg)
	
	def injectContributors(self):
		if 1:
			# use data from dlese_collect record
			# dlese_contribs = self.dcr.getEmailPrimaryContributors()
			dlese_contribs = self.dcr.getContributorsForContacts()
			dlese_support_found = False
			for contrib in dlese_contribs:
				if contrib.getEmail() == "support@dlese.org":
					dlese_support_found = True
				self.ncr.addContact(contrib)
				
			#ensure that dlese support is a contact
			if not dlese_support_found:
				self.ncr.addDleseSupportContact()
		else:
			# use dlese support as a contact
			self.ncr.addDleseSupportContact()
	
	def process_field_mappings (self):
		for mapping in self.field_mappings:
			if type(mapping) == type(''):
				self.injectField(mapping)
			elif type(mapping) == type([]):
				self.injectField(mapping[0], mapping[1])
			else:
				raise Exception,"Unknown mapping type: %s" % type(mapping)
	
	def testField(self, field):
		self.ncr.set(field, self.dcr.get(field))
		print 'ncr %s: %s' % (field, self.ncr.get(field))
		
	def testCreatedField(self):
		"""
		format of created value: 'T00:00:00Z'
		
		simply append string ('T19:42:03Z') to convert to dataTime format
		"""
		created = self.dcr.get('created')
		
		# convert to time_struct (not used)
		# createdTime = time.strptime(created, '%Y-%m-%d')
		# secs = time.mktime(createdTime)
		
		dateTime = created+'T00:00:00Z'
		
		# now as UTC
		self.ncr.set('dateTime', dateTime)
		
		print 'ncr %s: %s' % ('dateTime', self.ncr.get('dateTime'))
		
	def ensureInitialized (self):
		if not self.initialized:
			raise Exception, "not initialized"
		
	def __repr__ (self):
		return self.ncr.__repr__()
		
	def getRecord(self):
		return self.ncr
		
	def write(self, verbose=None):
		if self.ncr.path == self.ncs_collect_template:
			raise Exception, "Cowardly refusing to overwrite template"
		self.ncr.write()
		if verbose:
			print 'wrote to ', self.ncr.path
	
if __name__ == '__main__':
	
	from masterCollection import getDcrPath
	
	src = getDcrPath('dcc')
	
	# src = '/Users/ostwald/Desktop/DLESE_MIGRATION/dlese_collect/dlese_collect_tester.xml'
	transform = DleseToNcsCollectTransform(src, "OUTPUT")
	print transform
	transform.write(1)

	
	
