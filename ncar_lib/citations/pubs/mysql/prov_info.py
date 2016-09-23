"""
get unique country/prov codes contained in the pubs db

for each record, determine a code of the form country-prov by
combining the "meetstateprov" and "meetcountrycode" by a hypen

keep unique values
if country is null and prov isn't - print out message
if prov is null and country isn't - just use country
"""
import sys
from UserList import UserList
from UserDict import UserDict
from PubsDB import PubsDB, PublicationRec

class CodeError (Exception):
	pass

class Code:
	"""
	remember the country and prov components, but
	supply string representation like "country-prov" or just "country" if there
	isn't a prov
	"""
	def __init__ (self, country, prov):
		self.country = None
		self.prov = None
		if country is not None: self.country = country.strip()
		if prov is not None: self.prov = prov.strip()
		if not self.country:
			if not self.prov:
				raise KeyError, "no country or prov provided"
			else:
				raise CodeError, "country is None, prov is %s" % self.prov
				
	def __repr__ (self):
		if self.prov:
			return "%s-%s" % (self.country,  self.prov)
		else:
			return self.country or None
			
	def __cmp__ (self, other):
		"""
		support sorting by string representation
		"""
		return cmp(str(self), str(other))
	
class ProvInfoReporter(UserDict):
	"""
	reads country and province data from the Pubs database
	and reports unique values of country-prov
	
	self.data is a dict of code{str) -> code values
	"""
	def __init__ (self):
		UserDict.__init__ (self)
		self.codeErrors = []
		pubsDB = PubsDB()
		publications = pubsDB.getPubs ()
		print 'scanning %d publication records' % len(publications)
		for pub in publications:
			country = pub['meetcountrycode']
			prov = pub['meetstateprov']
			try:
				code = Code (country, prov)
				if not str(code):
					print "empty code: %s" % pub['pub_id']
					continue
				self.addCode (code)
			except KeyError:
				pass
			except CodeError:
				# print sys.exc_info()[1]
				self.codeErrors.append ("%s: %s" % (pub['pub_id'], sys.exc_info()[1]))
	
				
	def getCodes (self):
		"""
		sort the codes
		"""
		codes = self.values()
		codes.sort()
		return codes
				
	def addCode (self, code):
		"""
		we only want unique codes
		"""
		if not self.has_key (str(code)):
			self[str(code)] = code
			
	def reportErrors (self):
		if self.codeErrors:
			print "\nCode errors"
			for err in self.codeErrors:
				print "  ", err	
		else:
			print "no code errors"
			
	def report (self):
		"""
		separate the different codes by country
		"""
		self.reportErrors()
		
		print "\nUnique country-prov codes"
		currentCountry = ""
		for code in self.getCodes():
			if code.country != currentCountry:
				print "-"
				currentCountry = code.country
			print "  ", code

if __name__ == '__main__':
	ProvInfoReporter().report()

