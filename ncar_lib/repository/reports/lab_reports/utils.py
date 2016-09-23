import time

def unionDateToStruct (dateStr):
	struct = None
	for format in [ "%Y-%m-%d", "%Y-%m", "%Y" ]:
		try:
			struct = time.strptime (dateStr, format)
			break
		except:
			# print "couldn't parse as ", format
			pass
		
	if not struct:
		raise ValueError, 'could not parse "%s" as a date' % dateStr
				
	# print time.asctime(struct)
	return struct

def unionDateToSecs (dateStr):
	struct = unionDateToStruct(dateStr)
	return int (time.mktime(struct))
	
class FiscalYear:
	"""
	input - 2 or 4 digit integer
	repersents a fiscal year as data range
	
	- startDate, endDate are strings
	- start, end are timestamps (seconds)
	"""
	def __init__ (self, year):
		# year can be either a 2 or 4 digit number
		try:
			yearnum = int(year)
		except:
			raise Exception, "year (%s) must be a number" % year
		
		if yearnum < 100:
			yearnum = 2000 + yearnum
			
		self.startDate = "%d-10-01" % (yearnum-1)
		self.endDate = "%d-10-01" % yearnum
		
		self.start = unionDateToSecs (self.startDate)
		self.end = unionDateToSecs (self.endDate)
		
	def isLegalDate (self, unionDateStr):
		"""
		determines whether the provided date is with
		this fiscal year
		unionDateStr - 2010 or 2010-09 or 2010-09-87
		"""
		secs = unionDateToSecs (unionDateStr)
		return secs >= self.start and secs <= self.end
		
from ncar_lib.peopledb import InternalPersonSearch
		
def peopleDB_search (opts):
	"""
		example_params1 = {
			'firstName' : 'Greg',
			'lastName' : 'Holland'
		}
	"""
	print "Searching peopleDB ...."
	
	results = InternalPersonSearch(opts)
	print "%d people found for %s" % (len(results), opts)
	results.report()

if __name__ == '__main__':
	params = {
			'firstName' : 'Jim',
			'lastName' : "O'Neill"
		}
	peopleDB_search(params)
	
