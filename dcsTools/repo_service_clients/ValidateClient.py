"""
Get a list of the collections to validate, then invoke the DCSValidateService
"""

import sys, os, string, time
from JloXml import XmlRecord, XmlUtils
from dcsWebServiceClient import DCSWebServiceClient, DCSWebServiceClientError
from dds_client import ListCollections

verbose = True

def log (s) :
	if verbose:
		print s


def makeTimeString ():
	return time.strftime("%H:%M:%S, %m/%d/%Y ", time.localtime())
		
class ValidateClient (DCSWebServiceClient):
	verb = "ValidateCollection"
	required_params = ["collection"]
	
class Validator:
	
	dovalidate = False
	ping_interval = 10 # seconds
	
	def __init__ (self, host, xmlFormats=None, skipCollections=None):
		self.host = host
		print "Validator for '%s'" % host
		self.dcs_baseUrl = 'http://%s/schemedit/services/dcsws1-0' % host
		self.dds_baseUrl = 'http://%s/schemedit/services/ddsws1-1' % host
		self.xmlFormats = xmlFormats or []
		self.skipCollections = skipCollections or []
		
		# a list of collection Keys
		self.collections = self.getCollections()
		self.validate()
	
	def getCollections (self):
		"""
		xmlFormats (e.g., ['adn', 'osm']), when present, select collections.
		For example, ['adn', 'osm'] would select collections having adn or osm formats
		
		if the xmlFormats arg is absent, all collections are returned
		"""
		collections = ListCollections(self.dds_baseUrl).results
		log ("%d collections found" % len(collections))
		if self.xmlFormats:
			keys = map (lambda x:x.key, filter (lambda x:x.xmlFormat in self.xmlFormats, collections))
			log ( "%d collections after filtering by xmlFormat" % len(keys))
		else:
			keys = map (lambda x:x.key, collections)
		
		log ("now filter out skip_collections ..");
		keys = filter (lambda x:x not in self.skipCollections, keys)
		for key in keys:
			#log ( key )
			pass
		log ( "%d collections RETURNED from getCollections" % len(keys))
		return keys
		
	def validate (self):
		if self.dovalidate:
			print 'validating %d collections' % len(self.collections)
			for collection in self.collections:
				
				while 1:
					try:
						self.validateCollection(collection)
						print "\nVALIDATING %s ... (%s)" % (collection, time.asctime())
						break
					# except DCSWebServiceClientError, msg:
						# print "DCSWebServiceClientError: %s" % msg
						# sys.exit()
					except:
						print "  ... waiting to validate %s" % collection
						time.sleep(self.ping_interval)
						
		else:
			print 'collections that would have been validated'
			for collection in self.collections:
				print '- ', collection
				
	def validateCollection (self, collection):
		"""
		throws an exception if validation is busy
		"""
		params = {
			'collection' : collection
			}
			
		client = ValidateClient (self.dcs_baseUrl, params)
		rec = client.post()
		log (rec)

		
if __name__ == "__main__":
	host = 'ttambora.ucar.edu:10160'
	# host = 'nldr.library.ucar.edu'
	

	# xmlFormats =  ['osm_collect', 'citation']
	# skip_collections = ['1269906449928']
	
	xmlFormats =  []
	skip_collections = []
	
	validator = Validator(host, xmlFormats, skip_collections)
	
