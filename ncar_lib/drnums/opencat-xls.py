"""
create spreadsheet for openCat so they can map between the "uthbin"-form urls and citableUrls

http://www.library.ucar.edu/uhtbin/hyperion-image/DR000058

columns: uhtbin_url | citable_url | Accession_Number | nldr_collection_id | nldr_record_id

"""
import os, sys
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils
from urlparse import urlparse
import cgi

baseRepositoryUrl = "http://nldr.library.ucar.edu/repository"

class OpenCatXlsMaker (UserDict):
	
	def __init__ (self):
		UserDict.__init__ (self)
		rec = XmlRecord ('output/FINAL-accessionNumberMappings.xml')
		mappings = rec.selectNodes (rec.dom, 'accessionNumberMappings:mapping')
		print '%d mappings found' % len(mappings)
		for mapping in mappings:
			drNum = mapping.getAttribute("drNumber")
			queryString = mapping.getAttribute("queryString")
			# print '%s -> %s' % (drNum, queryString)
			self[drNum] = queryString
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
			
	def makeUhtbinUrl (self, drnum):
		return 'http://www.library.ucar.edu/uhtbin/hyperion-image/%s' % drnum
		
	def makeCitableUrl (self, queryString):
		params = cgi.parse_qs(queryString)
		for key in params:
			## values are lists
			# print "%s -> %s" % (key, params[key])
			pass
			
		return os.path.join (baseRepositoryUrl, params['collId'][0], params['itemId'][0])

	def makeRow (self, l):
		return '\t'.join (l)
		
	def asTabDelimited (self):
		rows=[];add=rows.append
		
		add (self.makeRow(['uhtbin_url', 'citable_url']))
		
		for drNum in self.keys():
			queryString = self[drNum]
			# print '%s -> %s' % (drNum, queryString)
			uhtbinurl = self.makeUhtbinUrl (drNum)
			citableUrl = self.makeCitableUrl (queryString)
			# print "\n%s\n  %s" % (uhtbinurl, citableUrl)
			add (self.makeRow([uhtbinurl, citableUrl]))
		return '\n'.join (rows)
		
	def write (self, path="output/urlMappings.txt"):
		fp = open (path, 'w')
		fp.write (self.asTabDelimited())
		fp.close()
		print "wrote to %s" % path
			
if __name__ == '__main__':
	xls = OpenCatXlsMaker()
	# print xls.asTabDelimited()
	xls.write()
		

