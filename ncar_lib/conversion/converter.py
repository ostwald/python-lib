"""
convert webcat to library_dc formats
"""
import os, sys
from ncar_lib.lib import globals, webcatUtils
from ncar_lib.lib.frameworks import LibraryDCRec
from webcatframework import WebcatRec
# import mapping.mapper
from mapping.mapper import Mapper
			
class Converter:

	"""
	Converts a WebcatRec instance to library_dc instance
	"""
	
	copy_fields = [
		"recordID",
		"url",
		"itemType",
		"description",
		"coverage",
		"creator",
		"contributor",
		"fullDescription",
		"subject",
		"scientificDivision",
		"dateOfOriginal",
		"dateItemDigitized",
		"date",
		"source",
		"format",
		"identifier",
		"language",
		"copyright"]
		
	def __init__ (self, webcat_rec):
		self.source = webcat_rec
		self.dest = LibraryDCRec()
		self.mapper = Mapper()
		
		for field in self.copy_fields:
			#val = self.source.getFieldValue (field)
			vals = self.source.getFieldValues (field)
			if vals:
				self.dest.addFieldValues (globals.field_mapping[field], vals)
			
		self.handlePubAndDiv()
		
		if (self.source.issue):
			self.dest.setFieldValue ("library_dc:issue", self.source.issue)
			
		if (self.source.fullTitle):
			self.dest.setFieldValue ("dc:title", self.source.fullTitle)
			self.dest.setFieldValue ("library_dc:altTitle", self.source.title)
		else:
			self.dest.setFieldValue ("dc:title", self.source.title)
			
		self.orderFields ()
		
	def mycmp (self, x, y):
		field_list = self.dest.field_list
		print "x: %s, y: %s" % (x.tagName, y.tagName)
		return cmp (field_list.index (x.tagName), field_list.index (y.tagName))
		
		
	def orderFields (self):
		# print "\nORDER FIELDS"
		elements = self.dest.doc.childNodes
		for e in elements:
			# print e.tagName
			pass
			
		# print "-------------"
		mycmp = lambda x, y:cmp (self.dest.field_list.index(x.tagName), 
								 self.dest.field_list.index(y.tagName))
		elements.sort(mycmp)
		for e in elements:
			# print e.tagName
			pass
		
	# see publisher-instructions-katy
	def handlePublisherOLD (self):
		"""
		replace publisher with mappings
		"""
		pmap = globals.publisher_mapping
		pubs = self.source.getFieldValues ("publisher")
		if not pubs:
			return
		for pub in pubs:
			if pmap.has_key (pub):
				mapping = pmap[pub]
				for key in ["instName", "instDivision"]:
					if mapping.has_key (key):
						self.dest.addFieldValue ("library_dc:" + key, mapping[key])
						## print "\t%s: %s" % ("library_dc:" + key, mapping[key])
			else:
				self.dest.addFieldValue ("library_dc:instName", pub)
				## print "\t%s: %s" % ("library_dc:instName", pub)
				
	def handlePubAndDiv (self):
		"""
		If there is not a mapping, add nothing
		if the mapping is an identity mapping, add InstName
		else add all instDivs and instNames for that mapping
		
		LATER we will remove all dups!
		"""
		publishers = self.source.getFieldValues ("publisher")
		scientificDivisions = self.source.getFieldValues ("scientificDivision")
		instNames = []
		instDivisions = []
		for vocab in publishers + scientificDivisions:
			# print "*** %s ***" % vocab
			if self.mapper.has_key (vocab):
				mapping = self.mapper.getMapping (vocab)
				# print mapping
				if mapping.isIdentity:
					# print "IDENTITY: " + vocab
					if not vocab in instNames:
						instNames.append (vocab)
					continue
				for instName in mapping.instNames:
					if not instName in instNames:
						instNames.append (instName)
				for instDiv in mapping.instDivs:
					if not instDiv in instDivisions:
						instDivisions.append (instDiv)	
			else:
				msg = "No mapping found for " + vocab
				# raise Exception, msg
		self.dest.setFieldValues ("library_dc:instName", instNames)
		self.dest.setFieldValues ("library_dc:instDivision", instDivisions)
			
		
def getConverter (id):
	path = utils.getRecordPath (id, "webcat")
	if not path:
		msg = "File not found for %s" % id
		raise Exception, msg
	return Converter (WebcatRec (path=path))
	
			
if __name__ == "__main__":
	c = getConverter ("MANUSCRIPT-000-000-000-805")
	print c.source
	print c.dest



