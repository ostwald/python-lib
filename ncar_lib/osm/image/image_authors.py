"""
see https://wiki.ucar.edu/display/opensky/IMAGe+Collection+Project"
"""

author_names = [
	# Current IMAGe Scientific Staff *
	'Jeffrey Anderson',
	'Doug Nychka',
	'Natasha Flyer',
	'Ram Nair',
	'Amik St-Cyr',
	'Hui Liu',
	'Steve Sain',
	'Rick Katz',
	'Linda Mearns',
	'Seth McGinnis',
	'Larry McDaniel',
	'Annick Pouquet',
	'Duane Rosenberg',
	'Pablo Mininni',
	
	# Past IMAGe Scientific Staff *',
	'Bo Li',
	'Yongku Kim',
	'Dorin Drignei',
	'Cari Kaufman',
	'Shree Khare',
	'Anders Malmberg',
	'Edwin Lee',
	'Aime Fournier',
	'Jonathan Pietarila Graham',
	'Eva Furrer',
	'Julien Baerenzung'
]

class ImageNameMatcher:
	"""
	able to determine whether a given name is contained in the image author list
	"""
	def __init__ (self):
		self.matchMap = self._build_match_list()
		
	def hasMatch (self, lastName, firstName):
		if not (lastName and firstName): return False
		# print "lastName: %s, firstName: %s" % (lastName, firstName)
		key = "%s,%s" % (lastName, firstName[0])
		return key in self.matchMap
		
	def hasMatchInList (self, authorList):
		"""
		authorList is list of ContributorPerson instances, which 
		have attributes including "lastName" and "firstName"
		"""
		for author in authorList:
			if self.hasMatch (author.lastName, author.firstName):
				return True
		return False
		
	def _build_match_list(self):
		"""
		the match list has entries of the form "<lastname>,<firstinitial>"
		"""
		matchList=[];add=matchList.append
		for author_name in author_names:
			splits = author_name.split()
			lastName = splits[-1]
			firstName = splits[0][0]
			add ("%s,%s" % (lastName, firstName))
		return matchList
		
nameMatcher = ImageNameMatcher()

if __name__ == '__main__':
	for author_name in author_names:
		splits = author_name.split()
		lastName = splits[-1]
		firstName = splits[0][0]
		print "%s : %s" % (author_name, nameMatcher.hasMatch (lastName, firstName))
		
	for author_name in ["Jonathan Ostwald"]:
		splits = author_name.split()
		lastName = splits[-1]
		firstName = splits[0][0]
		print "%s : %s" % (author_name, nameMatcher.hasMatch (lastName, firstName))		
