"""
 compares the ids defined in two versions of the same standards doc
"""
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

old_asnpath = os.path.join (asndir, "1995-NSES-v1.2.5-06012007.xml")
new_asnpath = os.path.join (asndir, "1995-NSES-v1.3.0-Science-082007.xml")

class AsnCompare:
	def __init__ (self):
		
		print "\nreading NEW standards"
		self.new_AsnStandards = StdDocument (new_asnpath)
		self.new_asn_ids = self.new_AsnStandards.keys()
		
		print "\nreading OLD standards"
		self.old_AsnStandards = StdDocument (old_asnpath)
		self.old_asn_ids = self.old_AsnStandards.keys()
		
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

		self.report_asn_diff()


if __name__ == "__main__":
	AsnCompare().report()
