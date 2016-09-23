from TabDelimitedRecord import TabDelimitedRecord
from TabDelimitedFile import TabDelimitedFile

path = '/home/ostwald/python-lib/ncar_lib/osm/wos/real_data/wos_ncar-ucar_fy11.txt'

def simpleDemo():
	"""
	path needs to be a tab-delmited file with a header row
	"""
	xsl = TabDelimitedFile ()
	xsl.read (path)
	
	print 'xls has %d records' % len (xsl)
	
class MyRecord (TabDelimitedRecord):
	"""
	exent WorksheetEntry to specify field delmiter, 
	to give class-specific attributes, etc
	"""
	pass
	
class MyTable (TabDelimitedFile):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	"""
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=MyRecord)
		self.read (path)
		
if __name__ == '__main__':
	table = MyTable (path)
	print "table has %d records" % len(table)
	table.showSchema()
	table.addField ("fooberry")
	table.showSchema()
	
	table[3]['fooberry'] = 'XXXXXXXXXXXXXXX'
	print table[3]
	print table[3]['fooberry']


