"""
parses WOS author data fields and produces an XML element that can be
inserted into an OsmRecord
"""
import sys, os, re
from JloXml import XmlUtils

def stripsplit (data, delimiter):
	"""
	strips white space from splits after splitting
	"""
	return map (lambda x:x.strip(), data.split(delimiter))

class AuthorParseException (Exception):
	pass
	
class Author:
	"""
	
	Parse data into name attrs (see self.attrs).
	
	- asElement produces element for osm.ContributorPerson
	
	- Do a look up of divisional information for every author to see if it can
	be determined. Then select the correct instDivision vocab term.
	"""
	attrs = ['lastName', 'firstName', 'middleName', 'secondMiddleName', 'suffix']
	
	def __init__ (self, data, authororder=None):
		"""
		data is the raw data from the spreadsheet for a single author
		
		- first and last names are separated by a comma, first, middle and second
		middle names may be full or a single letter with a period.
		  NOTES: 
			- sometimes first and last names are separated by a space.
			- see doc for processInitialias for rules employed
		"""
		self.data = data
		self.authororder = authororder
		self.initialized = False
		
		for attr in self.attrs:
			setattr (self, attr, '')
		
		# split data around comma
		splits = stripsplit (data, ',')
		
		if len(splits) == 1:  # no comma in original data
			# e.g., Xia Junrong
			splits2 = stripsplit (data, ' ')
			if len(splits2) != 2:
				raise AuthorParseException, 'expected two segments when split on space (%s)' % data
			self.firstName = splits2[0]
			self.lastName = splits2[1]
			self.initialized = True
			
		elif len(splits) == 3: # process suffix
			suffix = splits[2]
			# REMOVE trailing period (per Katy)
			if suffix[-1] == '.':
				suffix = suffix[:-1]
			# print "suffix: ", suffix
			self.suffix = suffix
			
		elif len(splits) != 2:
			raise AuthorParseException, 'data must have 1, 2 or 3 segments when split on comma'
			
		if len(splits) == 2 or len(splits) == 3:
			# so now we know there are either 2 or 3 splits
			self.lastName = splits[0]
			self.parseInitials (splits[1])

	def preprocessInitialsData (self, data):
		"""
		apply rule #1 (see parseInitials)
		"""
		rule1pat = re.compile (' -[A-Za-z]\.')
		
		data = rule1pat.sub (lambda m:m.group()[1:], data)
		return data
			
	def parseInitials (self, data):
		"""
		rules for parsing initials

		#1 - middle names starting with a hyphen (e.g., "Liu, T. -Y.") are run
		together with the first name (the space is eliminated). If the first
		name is an initial, retain the period after the first name.

			e.g. a - "Liu, T. -Y." becomes "Liu, T.-Y."
			e.g. b - "Liu, Tara -Y." becomes "Liu, Tara-Y."
			
			note: rule#1 is applied to the initials data in preprocessInitialsData
		
		#2 - initials of the form: "J-F." become "J.-F." (no spaces, period
		after each letter). This is an abbreviation of a hyphenated name such as
		Jeane-Francias)
		
		#3 - names of the form "A-F" (no period) become "A.-F." - no spaces.
		(these names are a variant of rule #2 above)
		
			note: rules #2 adn #3 are applied to nameSegments after the initials
			data is split into nameSegments (see processNameSegment)
		
		"""
		# print "before: %s" % data
		data = self.preprocessInitialsData(data)
		# print "after: %s" % data
		
		splits = stripsplit(data, ' ')
		if len(splits) > 0: # process firstName
			self.firstName = self.processNameSegment(splits[0])
			# if self.firstName[-1] == '.': self.firstName = self.firstName[:-1]
			if len(splits) == 1:
				self.initialized = True
		if len(splits) > 1: # process middleName
			self.middleName = self.processNameSegment(splits[1])
			# if self.middleName[-1] == '.': self.middleName = self.middleName[:-1]
			if len(splits) == 2:
				self.initialized = True
				
		if len(splits) > 2: # process secondMiddleName
			self.secondMiddleName = self.processNameSegment(splits[2])
			# if self.secondMiddleName[-1] == '.': self.secondMiddleName = self.secondMiddleName[:-1]
			if len(splits) == 3:
				self.initialized = True
				
		if len(splits) > 3:
			## we ignore all initials beyond secondMiddleName
			self.initialized = True
			
			# raise AuthorParseException, 'initials data has more than three segments'
		
	def processNameSegment (self, nameSegment):
		"""
		apply rules #2 adn #3 (see parseInitials)
		"""
		# rule #2
		rule2pat = re.compile ('[A-Za-z]-[A-Za-z]\.')
		if rule2pat.match (nameSegment):
			nameSegment = '%s.%s' % (nameSegment[:1], nameSegment[1:])
		
		rule3pat = re.compile ('([A-Za-z])-([A-Za-z])')	
		if len(nameSegment) == 3 and rule3pat.match(nameSegment):
			nameSegment = '%s.-%s.' % (nameSegment[0], nameSegment[2])

		if len(nameSegment) == 2 and nameSegment[-1] == '.':
			return nameSegment[:-1]
		else:
			return nameSegment
			
	def isAbreviation (self, nameSegment):
		"""
		used by the *display* methods (e.g., __repr__)
		nameSegment is a first, last or middleName.
		"""
		nameLengthTest = len(nameSegment) == 1
		hyphenTest = ('-' in nameSegment) and (len(nameSegment) < 4)
		
		# return nameLengthTest or hyphenTest
		return nameLengthTest
		# return (len(nameSegment) == 1) or (nameSegment[0] == '-')
			
	def __repr__ (self):
		"""
		display a name in human readable form.
		
		rules regarding periods in first, middle, and secondMiddleNames:
			display should add a period only when the name is a single letter,
			otherwise, no periods ..
		"""
		s = self.lastName
		if self.firstName or self.middleName:
			s = s + ","
		if self.firstName:
			s = "%s %s" % (s, self.firstName)
			# if len(self.firstName) == 1:
			if self.isAbreviation(self.firstName):
				s = s + '.'
		if self.middleName:
			s = "%s %s" % (s, self.middleName)
			# if len(self.middleName) == 1:
			if self.isAbreviation(self.middleName):
				s = s + '.'
		if self.secondMiddleName:
			s = "%s %s" % (s, self.secondMiddleName)
			#if len(self.secondMiddleName) == 1:
			if self.isAbreviation(self.secondMiddleName):
				s = s + '.'				
		if self.suffix:
			s = "%s, %s" % (s, self.suffix)
		# if self.authororder:
			# s = "%s (%d)" % (s, self.authororder)
		return s


	def asElement(self):
		element = XmlUtils.createElement('person')
		element.setAttribute ('role', 'Author')
		
		if self.authororder is not None:
			element.setAttribute ('order', str(self.authororder))
		
		for attr in self.attrs:
			tag = attr
			value = getattr(self, attr)
			if value:
				child = element.appendChild(XmlUtils.createElement(tag))
				XmlUtils.setText (child, value)
		return element
		
if __name__ == '__main__':
	author = Author ('Attie, J. -R.')
	print '%s (%s)' % (author, author.data)
	print author.asElement().toxml()
			
				
