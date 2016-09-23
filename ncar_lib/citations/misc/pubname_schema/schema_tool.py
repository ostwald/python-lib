"""
adds a list of vocab values to an existing schema, and creates a new schema
- only new values are added
- values are sorted
"""

from PubNameXSD import PubNameXSD, getPubNameSchema


class SchemaTool:
	"""
	master schema has a class and a path
	new terms is a list of terms
	"""
	
	def __init__ (self, schema, newTerms):
		self.master = schema
		self.newTerms = newTerms
		
	def makeTermlist (self):
		terms = self.master.getPubNames()
		for term in self.newTerms:
			if term not in terms:
				terms.append (term)
		terms.sort()
		return terms
		
	def getNewSchemaRec (self):
		self.master.setPubNames (self.makeTermlist())
		return self.master
		
		
def getNewTermList ():
	from ncar_lib.citations.citations_values import UniqueValues
	field = 'pubname'
	startDir = "/home/ostwald/python-lib/ncar_lib/citations/pubs/PUBS_other_metadata"
	return UniqueValues (startDir, field).values
	
		
if __name__ == '__main__':
	newTerms = getNewTermList ()
	tool = SchemaTool (getPubNameSchema(), newTerms)
	print "%d master terms" % len(tool.master.getPubNames())
	print "%d new terms" % len (newTerms)
	newSchema = tool.getNewSchemaRec()
	print "%d new schemaTerms" % len (newSchema.getPubNames())
	for v in newSchema.getPubNames():
		print v
