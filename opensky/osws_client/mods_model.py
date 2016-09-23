"""
fields we need to expose for cvs output
- genre
- ark
- publication year (keyDate
"""
import os, sys
from lxml import etree
from UserList import UserList

__author__ = 'ostwald'

class Name:
	"""
	we need to know
	- role
	- type (personal|corporate)
	   - these are for authors. other Name types include
	- isAuthor
	- isNcarAuthor
	- display_name (depends on type
	"""
	def __init__ (self, element, namespaces):
		self.element = element
		self.namespaces = namespaces

		self.role = self._get_role()
		self.type = self.element.get('type')
		self.isAuthor = self.role and self.role.lower() == 'author' or False
		self.upid = self.isAuthor and self.element.get('valueURI', None) or None
		self.isNcarAuthor = self.upid is not None
		self.displayName = self._get_display_name()

	def _get_role (self):
		"""
		some Name types (e.g., conference) have no role
		"""
		try:
			return self.element.xpath("mods:role/mods:roleTerm[@type='text']", namespaces=self.namespaces)[0].text;
		except:
			pass

	def _get_display_name (self):
		if self.type == 'personal':
			return self._format_person_name()
		return self._get_text_at_path("mods:namePart")
		# else:
		# 	try:
		# 		return self.element.xpath("mods:namePart", namespaces=self.namespaces)[0].text
		# 	except:
		# 		pass

	def _format_person_name (self):
		# first = ''
		# last = ''
		# first_q = self.element.xpath("mods:namePart[@type='given']", namespaces=self.namespaces)
		# last_q = self.element.xpath("mods:namePart[@type='family']",namespaces=self.namespaces)
		# # last = XmlUtils.getTextAtPath(node, "namePart[@type='family']")

		first = self._get_text_at_path("mods:namePart[@type='given']")
		last = self._get_text_at_path("mods:namePart[@type='family']")

		s = last
		if last and first and len(first):
			s += ', %s.' % first[0]
		return s
		# if first_q and len(first_q):
		# 	first = first_q[0].text
		# if last_q and len(last_q):
		# 	last = last_q[0].text
		# return '%s, %s.' % (last, first)

	def _get_text_at_path (self, xpath, default=None):
		try:
			return self.element.xpath(xpath, namespaces=self.namespaces)[0].text
		except:
			return default

	def __repr__ (self):
		s = [];add=s.append
		add ('\nNAME - %s' % self.displayName)
		attrs = 'role', 'type', 'isAuthor', 'upid', 'isNcarAuthor'
		for attr in attrs:
			add ('- %s: %s' % (attr, getattr(self, attr)))
		return '\n'.join(s)

class Names (UserList):
	"""
	provide access to Names objects
	- getAuthors (optional type)
	"""
	def __init__(self, elements, namespaces):
		self.data = []

		# print 'Names: processing elements'
		for el in elements:
			self.data.append (Name (el, namespaces))

	def get_authors (self):
		return filter (lambda x:x.isAuthor, self)

class ModsRecord:

	MAX_AUTHORS_TO_SHOW = 3

	namespaces = {
		'ns0': 'http://www.openarchives.org/OAI/2.0/',
		'mods' : "http://www.loc.gov/mods/v3",
		'xlink' : "http://www.w3.org/1999/xlink",
	    'osm' : 'http://nldr.library.ucar.edu/metadata/osm'
	}

	def __init__ (self, xml):
		self.root = etree.fromstring(xml)
		self.names = self._get_names()

	def __repr__ (self):
		return etree.tostring(self.root)

	def get_title (self):
		# return self.getTextAtPath('mods:titleInfo:title')
		return self.getXpath('/mods:mods/mods:titleInfo/mods:title')

	def get_genre (self):
		return self.getXpath('/mods:mods/mods:genre')

	def get_journal(self):
		return self.getXpath("/mods:mods/mods:relatedItem[@type='host']/mods:titleInfo/mods:title")

	def get_collaboration(self):
		return self.getXpath("/mods:mods/mods:extension/osm:collaboration")

	def _get_names(self):
		selector = '/mods:mods/mods:name'
		# selector = "/mods:mods/mods:name[@type='personal']"
		return Names(self.root.xpath(selector, namespaces=self.namespaces), self.namespaces)

	def get_ncar_authors(self):
		return filter (lambda x:x.upid, self.names.get_authors())

	def get_authors_display (self, authors=None):
		"""
		returns a list of displayNames for provided authors,
		truncated to MAX_AUTHORS_TO_SHOW
		"""
		authors = authors or self.names.get_authors()
		author_names = map (lambda x:x.displayName, authors)
		if not author_names:
			return 'no authors found'
		elif len(author_names) < self.MAX_AUTHORS_TO_SHOW + 1:
			return '; '.join(author_names)
		else:
			return '; '.join(author_names[:self.MAX_AUTHORS_TO_SHOW]) + '; et al'


	def normalize_value(self, val):
		norm = val.strip().replace('\n','')
		while norm.find('  ') != -1:
			norm = norm.replace('  ', ' ')
		return norm
	#
	# def getTextAtPath (self, path):
	# 	val = XmlRecord.getTextAtPath(self, path)
	# 	return self.normalize_value(val)

	def getXpath (self, xpath, namespaces=None):
		namespaces = namespaces or self.namespaces
		try:
			return self.normalize_value(self.root.xpath(xpath,
			                       namespaces=namespaces)[0].text)
		except IndexError, msg:
			# nothing found at path
			# print 'WARN: %s' % msg
			return None

if __name__ == '__main__':
	# path='xml_samples/mods-sample.xml'
	path='xml_samples/conference_2777_mods.xml'
	xml = open(path, 'r').read()
	rec = ModsRecord (xml)
	# print rec
	if 1:
		print 'TITLE:', rec.get_title()
		authors = rec.get_authors_display()
		print 'AUTHORS:', authors
		print 'JOURNAL:', rec.get_journal()
		print 'COLLABORATION:',rec.get_collaboration()
		print 'NCAR AUTHORS UPIDS: %s' % ', '.join(rec.get_ncar_author_upids())

	if 0:
		print 'Authors'
		for name in rec.names.get_authors():
			print name

	ncar_authors = rec.get_ncar_authors()
	for author in ncar_authors:
		print ' - %s - %s' % (author.upid, author.displayName)