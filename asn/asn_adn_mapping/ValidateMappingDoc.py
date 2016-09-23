import sys, os
import urllib
from JloXml import XmlRecord
from asn import StdDocument
from asn.util import getNumId

print sys.platform

if sys.platform == 'win32':
	asndir = "H:/python-lib/asn/standards-documents/localized"
else:
	asndir = "/home/ostwald/python-lib/asn/standards-documents/localized"

new_asnpath = os.path.join (asndir, "1995-NSES-v1.2.5-06012007.xml")
old_asnpath = os.path.join (asndir, "1995-NSES-v1.2.5-012007.xml")

mappings_url = "http://www.dlese.org/Metadata/documents/xml/ADN-ASN-v1.2.5-NSES-mappings.xml"

class Validator (XmlRecord):
	def __init__ (self, url):
		self.url = url
		XmlRecord.__init__ (self, xml=self.getUrl (url))
		self.mapped_ids = self._getMappedIds ()
		
		print "\nreading NEW standards"
		self.new_AsnStandards = StdDocument (new_asnpath)
		self.new_asn_ids = self.new_AsnStandards.keys()
		
		print "\nreading OLD standards"
		self.old_AsnStandards = StdDocument (old_asnpath)
		self.old_asn_ids = self.old_AsnStandards.keys()

	def _getMappedIds (self):
		mappings = self.selectNodes (self.dom, "Adn-to-Asn-mappings:mapping")

		print "%d mappings found" % len (mappings)
		ids = map (lambda a: a.getAttribute ("asnIdentifier"), mappings)
## 		for id in ids:
## 			print "\t", id
		ids.sort()
		return ids

		
	def set_diff (self, set1, set2):
		ids = []
		add = ids.append
		for id in set1:
			if id not in set2:
				add (id)
		return ids
		
	def new_asn_not_in_old_asn (self):
		ids = self.set_diff (self.new_asn_ids, self.old_asn_ids)
		return self.filter_ids_by_level (ids, self.new_AsnStandards)
		
	def old_asn_not_in_new_asn (self):
		ids = self.set_diff (self.old_asn_ids, self.new_asn_ids)
		return self.filter_ids_by_level (ids, self.old_AsnStandards)
		
	# filter threshold for mapping files is 2, since mapping contains only levels 3 and 4
	def mapping_not_in_new_asn (self):
		ids = self.set_diff (self.mapped_ids, self.new_asn_ids)
		return self.filter_ids_by_level (ids, self.old_AsnStandards, 2)
		
	# filter threshold for mapping files is 2, since mapping contains only levels 3 and 4
	def mapping_not_in_old_asn (self):
		ids = self.set_diff (self.mapped_ids, self.old_asn_ids)
		return self.filter_ids_by_level (ids, self.old_AsnStandards, 2)
		
	# filter threshold for mapping files is 2, since mapping contains only levels 3 and 4
	def new_asn_not_in_mapping (self):
		ids = self.set_diff (self.new_asn_ids, self.mapped_ids)
		return self.filter_ids_by_level (ids, self.new_AsnStandards, 2)
	
	# filter threshold for mapping files is 2, since mapping contains only levels 3 and 4
	def old_asn_not_in_mapping (self):
		ids = self.set_diff (self.old_asn_ids, self.mapped_ids)
		return self.filter_ids_by_level (ids, self.old_AsnStandards, 2)
		
	def report_new (self):
		ids = self.mapping_not_in_new_asn()
		if ids:
			print "\nIds in Mapping but not in NEW ASN doc (%d)" % len (ids)
			for id in ids:
				std = self.old_AsnStandards[id]
				print "\t%s level: %d" % (getNumId(id), std.level + 1)
		else:
			print "\nAll Ids in mapping are present in NEW ASN doc"
		
		ids = self.new_asn_not_in_mapping()
		if ids:
			print "\nIds in NEW ASN but not in Mapping (%d)" % len (ids)
			for id in ids:
				std = self.new_AsnStandards[id]
				print "\t%s level: %d" % (getNumId(id), std.level + 1)
		else:
			print "\nAll NEW ASN Ids are present in mapping doc"

	def report_old (self):
		ids = self.mapping_not_in_old_asn()
		if ids and 0:
			print "\nIds in Mapping but not in OLD ASN doc (%d)" % len (ids)
			for id in ids:
				std = self.old_AsnStandards[id]
				print "\t%s level: %d" % (getNumId(id), std.level + 1)
		
		ids = self.old_asn_not_in_mapping()
		if ids:
			print "\nIds in OLD ASN but not in Mapping (%d)" % len (ids)
			for id in ids:
				std = self.old_AsnStandards[id]
				print "\t%s level: %d" % (getNumId(id), std.level + 1)
		
	def report_asn_diff (self):
		ids = self.new_asn_not_in_old_asn()
		if 1:
			print "\nNEW ASN stds not in OLD ASN stds (%d)" % len (ids)
			for id in ids:
				std = self.new_AsnStandards[id]
				print "\t%s level: %d" % (getNumId(id), std.level + 1)	
				
		ids = self.old_asn_not_in_new_asn()
		if 1:
			print "\nOLD ASN stds not in NEW ASN stds (%d)" % len (ids)
			for id in ids:
				std = self.old_AsnStandards[id]
				print "\t%s level: %d" % (getNumId(id), std.level + 1)					
		
	def filter_ids_by_level (self, ids, standardsDoc, threshold=None):
		"""
			1 - sort the ids as strings (just to put them in some consistent order)
			2 - filter out the standards for level less than threshold (if provided)
			3 - sort by level (in standards hierarchy)
		"""
		filtered = []
		ids.sort()
		for id in ids:
			level = standardsDoc[id].level + 1
			if threshold:
				if level > threshold:
					filtered.append (id)
			else:
				filtered.append (id)
		return self.sort_by_level (filtered, standardsDoc)
				
	def sort_by_level (self, ids, standardsDoc):
		bins = {}
		for id in ids:
			level = standardsDoc[id].level + 1
			if not bins.has_key(level):
				bins[level] = []
			items = bins[level]
			items.append (id)
			bins[level] = items
		sorted_ids = [];add=sorted_ids.append
		for level in bins.keys():
			items = bins[level]
			for id in items:
				add (id)
		return sorted_ids
		
	def report (self):
		self.report_new()
		self.report_old()
		self.report_asn_diff()
				
	def getUrl (self, url):
		try:
			data = urllib.urlopen(url)   # open file by url
			return data.read()

		except IOError, error_code :		# catch the error
			if error_code[0] == "http error" :
				print "error: ", error_code[1]
				# print error_code				




if __name__ == "__main__":
	
	mappings = Validator (mappings_url)
	# mappings.report()
	mappings.report_new()
