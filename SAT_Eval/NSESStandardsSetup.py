"""
NSES Standards Setup
- All 4th Level Standards EXCEPT "Unifying Standards", split up into
domain_groups, which in turn are split up into gradeRange bands.

the resulting structure is then written to file as NSESStandardsPool.py, where standards
are then randomly selected by SelectedStandards
"""
import sys, os, string
from UserDict import UserDict
from asn import StdDocument, AsnStandard
from sat_utils import *

standardsDir = "/home/ostwald/python-lib/asn/standards-documents/localized/"

NSESpath = os.path.join (standardsDir, "1995-NSES-v1.2.5-012007.xml")

class GradeRangeMap (UserDict):
	
	def add (self, item):
		gradeRange = str (item.gradeRange)
		if not self.has_key (gradeRange):
			self[gradeRange] = []
		self[gradeRange].append(item)

	def keys (self):
		ks = self.data.keys();
		ks.sort (band_cmp)
		return ks
	
	def report (self):
		for key in self.keys():
			print "%s (%d)" % (key, len (self[key]))
			# for std in self[key]:
				# print "\t%s" % std.numId
	
class SubjectGroupMap (UserDict):
	"""
	keys are Bands
	"""

	def _getGroup (self, domain):
		for key in domain_groups.keys():
			if domain in domain_groups[key]:
				return key
				
	def add (self, item):
		group = self._getGroup (item.std_domain)
		if not self.has_key(group):
			self[group] = GradeRangeMap()
		
		self[group].add (item)
	
	def report (self):
		print "SubjectGroupMap"
		for band in domain_groups_keys:
			print "** %s **" % band
			self[band].report()
				
	
class NSESStandardsSetup (UserDict):
	
	def __init__ (self, path):
		UserDict.__init__(self);
		self.NSES = StdDocument (NSESpath)
		self.groups = SubjectGroupMap()
		self._init_pool ()

		
		# for i in range(10):
			# std = self.pool[i]
			# # print "%s: %s" % (getBand(std), std.description)
			# print self._get_std_domain (std)
		

	def add (self, item):
		self[item.id] = item
		self.groups.add (item)
			
	def _init_pool (self):

		for asnStd in self.NSES.values():
			if asnStd.level == 3:
				std_domain = self._get_std_domain (asnStd)
				if std_domain:
					self.add(NSESStandard (asnStd, std_domain))

		
	def _get_std_domain (self, std):
		# print "getBand(): " + std.description
		domains = nses_std_domains.keys()
		node = std
		while node and node.description not in domains:
			node = self.NSES[node.parent]
		if node and node.description in domains:
			return nses_std_domains[node.description]
			
	def __repr__ (self):
		s=[];add=s.append
		
		add ("NSES_stds_pool = {");
		for group_name in domain_groups_keys:
			add ('\t"%s": {' % group_name)
			
			group = self.groups[group_name]
			for band_name in group.keys():
				add ('\t\t"%s" : [' % band_name)
				
				band = group[band_name]
				for std in band:
					add ('\t\t\t"%s",' % std.numId)
				add ('\t\t],')
			add ('\t},')
		add ('}')
		return string.join (s,"\n")

class NSESStandard:
	def __init__ (self, asnStd, std_domain):
		self.id = asnStd.id
		self.children = asnStd.children
		self.parent = asnStd.parent
		self.description = asnStd.description
		self.gradeRange = str(asnStd.gradeRange)[1:-1]
		self.level = asnStd.level + 1
		self.numId = getNumId (self.id)
		self.std_domain = std_domain
			
if __name__ == "__main__":
	
	pool = NSESStandardsSetup (NSESpath)
	
	print "%d standards in pool" % len (pool)
	pool.groups.report()
	f = open ("NSESStandardsPool.py", 'w')
	f.write (pool.__repr__())
	f.close()
