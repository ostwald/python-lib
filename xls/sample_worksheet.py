from XslWorksheet import XslWorksheet, WorksheetEntry

path = '/Documents/Work/NCAR Lib/OpenSky/AMS Scrape/AMS.J.high.cited.txt'

def simpleDemo():
	"""
	path needs to be a tab-delmited file with a header row
	"""
	xsl = XslWorksheet ()
	xsl.read (path)
	
	print 'xls has %d records' % len (xsl)
	
class MyRecord (WorksheetEntry):
	"""
	exent WorksheetEntry to specify field delmiter, 
	to give class-specific attributes, etc
	"""
	pass
	
class MyWorkSheet (XslWorksheet):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	"""
	def __init__ (self, path):
		XslWorksheet.__init__ (self, entry_class=MyRecord)
		self.read (path)
		
if __name__ == '__main__':
	ws = MyWorkSheet (path)
	print "ws has %d records" % len(ws)


