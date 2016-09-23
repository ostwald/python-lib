"""
create osm's instDiv XSD vocab file using values from UCAR People.organization table

each org is of form
	- "% (%)" % (org.full_name, org.abbreviation)
	
vocab values are orgs joined together by colon.

- write the xsd file to disk
"""
import os, sys
from ncar_lib.osm.vocabs.xsd import VocabXSD

sys.path.append ('/Volumes/InfoSpace/Documents/Work/NCAR Lib/OpenSky/orgChart')
from org_tree import OrgTree, OrgNode

verbose = False

class PubsOrgVocabs (OrgTree):
	"""
	as an OrgTree, we provide indexed access to nodes, and tree-oriented
	functions
	
	this Class adds the ability to expose vocabs so they can be used to create
	an instDiv.xsd vocab file
	"""
	def __init__ (self):
		"""
		provide "vocabs", a sorted list of vocab values defined by the orgs
		in this orgTree
		"""
		OrgTree.__init__ (self)
		self.vocabs = []
				
		self.makeVocabs (self.getLabs())
		self.vocabs.sort()
		
	def makeVocabs (self, items):
		"""
		recursively traverse orgTree to produce data in a form digestible by 
		InstDivXSD.setInstDivValues()
		
		- adds a vocab term derived from each orgNode encountered
		"""
		for item in items:
			if item is None: continue
		
			if verbose:
				print "\n(%d) - %s" % (item.id, self.getVocab(item.id))
				
			# add vocab term to global list
			self.vocabs.append (self.getVocab(item.id))
			
			if item.children:
				self.makeVocabs (map (self.__getitem__, item.children))
	
	def showVocabs(self):
		"""
		print a list of the vocabs in this tree
		"""
		for v in self.vocabs:
			print '\n', v

class InstDivXSD (VocabXSD):
	"""
	class responsible for creating and writing an "instDiv.xsd" file
	using organizational information from the People database
	
	- reads in an instDiv.xsd template file
	- modifies xsd to reflect organizational structure defined in PeopleDB
	- writes new xsd to file
	
	"""
	xsd_template_path = 'xsd/instDivision-TEMPLATE.xsd'

	def __init__ (self):
		"""
		as an XSD we have access to the vocab values in the source xsd
		"""
		VocabXSD.__init__ (self, self.xsd_template_path)
		
		self.typeName = "instDivisionType"
		self.instDiv = self.getEnumerationType(self.typeName)
		assert self.instDiv is not None
			
		
	def setInstDivValues (self, vocabItems):
		"""
		vocabItems is a list of vocab values that will
		replace any existing vocab values in this file
		"""
		self.setEnumerationValues (self.typeName, vocabItems)
		
	def getInstDivValues (self):
		"""
		gets the values of the instDiv vocab
		"""
		return self.getEnumerationValues(self.typeName)
		
	def write (self, path):
		"""
		write the xsd record to file at specified path
		"""
		VocabXSD.write (self, path, verbose=True)
		
class  PubsInstDivXSDWriter (InstDivXSD):
	"""
	populates and writes InstDiv XSD with vocabs pulled from the UCAR orgChart
	 - see PubsOrgVocabs
	"""		
	
	dowrites=1
	
	def __init__(self, outpath):
		InstDivXSD.__init__ (self)
	
		vocabs = PubsOrgVocabs().vocabs
		self.setInstDivValues(vocabs)
		if 1:
			self.write (outpath)
		else:
			print self
		
if __name__ == '__main__':
	PubsInstDivXSDWriter("xsd/TEST-InstDiv.xsd")
