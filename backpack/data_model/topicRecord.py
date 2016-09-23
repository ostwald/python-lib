"""
TopicRecord
- input: xml (an html table) containing a header and then data rows, 
each representing a top-pick.
- output:
	parsed_data is a list of rows (each of which is a list)
	- the first row is a header
	- the rest data for top-picks
"""
import os, sys, re, codecs
from JloXml import XmlRecord, XmlUtils
import utils

class NoTopPickDataError (Exception):
	pass

class TopicRecord (XmlRecord):
	
	xpath_delimiter = '/'
	default_encoding = utils.html_data_encoding
	
	def __init__ (self, table_html, encoding=None):
		self.encoding = encoding or self.default_encoding
		table_html=table_html.replace ('&nbsp', ' ')
		try:
			XmlRecord.__init__ (self, xml=table_html, encoding=self.encoding)
		except:
			print '\topicRecord: XmlRecord couldnt parse table xml - halting'
			bog = 'bogus-table-html.xml'
			fp = codecs.open(bog, 'w', self.encoding)
			fp.write (table_html)
			fp.close()
			print 'wrote to', bog
			sys.exit()
		
		self.parsed_data = self.parse()
		
	def parse (self):
		rows = self.selectNodes (self.dom, 'table/tr')
		print '%d rows found' % len(rows)
		table_data = []
		if len(rows) < 2: # no data for this topic!
			raise NoTopPickDataError, 'No data found'
		for i, row in enumerate(rows):
			try:
				table_data.append(self.getRowCells(row, i))
			except NoTopPickDataError, msg:
				# print "skipped a blank row (%s)" % msg
				pass
		return table_data
		
	def writeTabDelimited (self, path):
		td_rows = map (lambda x:'\t'.join(x), self.parsed_data)
		s = '\n'.join(td_rows)
		fp = codecs.open (path, 'w', 'utf-8')
		fp.write (s.encode('utf-8'))
		fp.close()
		print 'wrote to', path
		
	whiteSpacePat = re.compile('[\s]')
		
	def cleanCellData (self, s):
		return ' '.join(filter (None, self.whiteSpacePat.split(s)))
		
	def getRowCells (self, row, rowNum):
		cells = self.selectNodes(row, 'td')
		data = [];add=data.append
		for i, cell in enumerate(cells):
			if i == 1:
				if rowNum == 0:  # hdr
					add (XmlUtils.getText(cell))
					add ('url')
				else:
					link = XmlUtils.getChild ('a', cell)
					if link == None:
						if rowNum == 1:
							add ('')
							add ('')
							continue
						else:
							raise NoTopPickDataError, 'No link found in row %d' % rowNum
					
					add (XmlUtils.getText(link))
					add (link.getAttribute('href'))
			else:
				add (XmlUtils.getText(cell))
			
		return map (self.cleanCellData, data)
				
	def report (self):
		
		for rowNum, row in enumerate(self.parsed_data):
			print '\nRow %d' % rowNum
			for cellNum, cell in enumerate(row):
				print '- %d - %s' % (cellNum, cell)
		
		
if __name__ == '__main__':
	xml = open('data-table.xml','r').read()
	xml=xml.replace ('&nbsp', ' ')
	data = TopicRecord (xml)
	data.report()
	# data.writeTabDelimited ('data_table-TEST.txt');
	# print data
