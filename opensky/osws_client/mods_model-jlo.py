__author__ = 'ostwald'
"""
fields we need to expose for cvs output
- genre
- ark
- publication year (keyDate
"""
from JloXml import XmlRecord, XmlUtils

class ModsRecord (XmlRecord):

	MAX_AUTHORS_TO_SHOW = 3

	def get_title (self):
		return self.getTextAtPath('mods:titleInfo:title')

	def get_genre (self):
		return self.getTextAtPath('mods:genre')

	def get_journal(self):
		return self.getTextAtPath("mods:relatedItem[@type='host']:titleInfo:title")

	def get_collaboration(self):
		return self.getTextAtPath("mods:extension:collaboration")

	def get_authors (self):
		nodes = self.selectNodes(self.dom, 'mods:name')
		print '%d name nodes found' % len(nodes)

		def format_name (node):
			print 'format_name'
			first = XmlUtils.getTextAtPath(node, "namePart[@type='given']")
			last = XmlUtils.getTextAtPath(node, "namePart[@type='family']")

			return '%s, %s.' % (last, first[0])

		author_names = map (format_name, nodes)
		if len(author_names) < self.MAX_AUTHORS_TO_SHOW + 1:
			return ';'.join(author_names)
		else:
			return ';'.join(author_names[:self.MAX_AUTHORS_TO_SHOW]) + ';et al'

	def normalize_value(self, val):
		norm = val.strip().replace('\n','')
		while norm.find('  ') != -1:
			norm = norm.replace('  ', ' ')
		return norm

	def getTextAtPath (self, path):
		val = XmlRecord.getTextAtPath(self, path)
		return self.normalize_value(val)

if __name__ == '__main__':
	rec = ModsRecord (path='mods-sample.xml')
	print rec.get_title()
	authors = rec.get_authors()
	print authors
	print rec.get_journal()
	print rec.get_collaboration()
	# norm = rec.normalize_value(rec.get_title())
	# print 'NORM: %s' % norm
