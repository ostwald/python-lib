"""
Represents a result from the osws

the OSWSResult.payload is a ModsRecord

fields we need to expose for cvs output
- from payload (ModsRecord)
	- genre
	- title
	- authors (ultimately we want authors (Lastname, F.) joined by ';'. If more than three, et al
	- journal
	- collaboration
- from header
	- publication year (keyDateYMD)
	- doi
	- ark

"""
__author__ = 'ostwald'
from JloXml import XmlRecord, XmlUtils
from mods_model import ModsRecord

class ResultToCsvMixin:
	"""
	header must be named for Result class attributes. E.g., if header field is 'title', then
	Result class must have attribute named 'title'
	"""
	headers = [
		# 'pid', # for debugging
		# 'pub_type', #non-informative (they're all article)
		'pub_date',
		'title',
		'authors',
		'doi',
		'ark',
		'journal',
		'collaboration',
		'num_yellowstone_authors',
		'yellowstone_authors',
		'sum_author_charges',
		'other_ncar_authors',
	]

	def toCsv (self):
		values = [];add=values.append
		for attr in self.headers:
			# print '- attr: %s' % attr
			value = getattr (self, attr) or ''
			# print ' val(raw): %s' % value

			# lists are joined by comma
			try:
				# if attr == 'ncar_author_upids':
				if attr == 'ark':
					value = 'http://n2t.net/%s' % value
				elif type(value) == type([]):
					value = '"%s"' % ', '.join(value)
				else:
					if type(value) == type(0) or type(value) == type(1.0):
						value = str(value)
					else:
						# santize by removing double quotes
						value = value.replace('"', '')
						# now add quotes if value contains comma
						if value.find(',') != -1:
							value = '"%s"' % value
						# if value.find(',') != -1 and value[0] != '"' and value[0] != "'":
						# 	if value.find ("'") == -1:
						# 		value = '"%s"' % value
						# 	elif value.find ('"') == -1:
						# 		value = "'%s'" % value


						# if value.find('"') != -1:
						# 	value = "'%s'" % value
						# elif value.find ("'") != 1:
						# 	value = '"%s"' % value
			except Exception, msg:
				print 'could not handle value: (%s): %s' % (value, msg)
				value = "??"
			add (value)
		return ','.join(values)

class OSWSResult(XmlRecord, ResultToCsvMixin):
	"""
	exposes:
		- pid
		- payload (an ModsRecord instance)
	"""
	default_payload_constructor = ModsRecord

	def __init__ (self, xml, payload_constructor=None):
		self.payload_constructor = payload_constructor or self.default_payload_constructor
		# XmlRecord.__init__ (self, xml=element.toxml())  # xml is an Jlo Element
		XmlRecord.__init__ (self, xml=xml) # xml is a string
		# self.recId = self.getTextAtPath("head:id")
		self.pid = self.get_header_field("PID")
		self.pub_date = self.get_header_field("keyDateYMD")
		self.ark = self.get_header_field("ark")
		self.doi = self.get_header_field("doi")

		# get values from payload
		self.payload = self.get_payload ()
		self.title = self.payload.get_title()
		self.pub_type = self.payload.get_genre()
		self.journal = self.payload.get_journal()
		self.collaboration = self.payload.get_collaboration()

		try:
			self.authors = self.payload.get_authors_display()
		except:
			print 'could not get get_authors_display for %s' % self.pid
			self.authors = 'no authors found'

		self.ncar_authors = self.payload.get_ncar_authors()
		# self.ncar_author_names = self.payload.get_authors_display(self.ncar_authors)
		# self.num_ncar_authors = len(self.ncar_authors)
		# self.ncar_author_upids = map(lambda x:x.upid, self.ncar_authors)

		# these fields must be populated externally (e.g., by Reporter)
		self.sum_author_charges = 0
		self.num_yellowstone_authors = ''
		self.yellowstone_authors = ''
		self.sum_author_charges = ''
		self.other_ncar_authors = ''

	def get_header_field(self, field):
		return self.getTextAtPath("result:head:" + field.strip())

	def get_payload (self):
		"""
		we can't select mods (because of namespaces?) so we first grab the
		metadata node and build payload from first child (the mods element)
		"""
		metadata = self.selectSingleNode (self.dom, "result:metadata")
		if not metadata:
			raise Exception, "Could not find metadata"
		children = XmlUtils.getChildElements(metadata)
		if not children:
			raise Exception, "Could not find payload"
		if len(children) != 1:
			raise Exception, "Found multiple payload elements"
		return self.payload_constructor (xml=children[0].toxml())

	def get_collection (self):
		node = self.selectSingleNode (self.dom, "record:head:collection")
		if node:
			return node.getAttribute("key")

	def report(self):
		print '\n%s REPORT' % self.pid
		for attr in ['pub_date', 'ark','doi']:
			print '- %s: %s' % (attr, getattr(self, attr))

if __name__ == '__main__':
	path = 'xml_samples/result-sample.xml'
	content = open(path, 'r').read()
	result = OSWSResult(content)
	print result.toCsv()