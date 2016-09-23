from nsdl.bppb_redirect.rewrite_rules import URL, RedirectMapping, RedirectTable
from UserDict import UserDict

class BPPBMappings (UserDict):
	
	default_path = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/BPPB_Redirects/Final_Redirect_Table.txt'
	
	def __init__ (self, path=None, strict=False):
		self.path = path or self.default_path
		self.strict = strict
		self.data = {}
		RedirectTable.linesep = '\r' # working on mac at home
		for mapping in RedirectTable (self.path):
			old = mapping['Old URL']
			new = mapping['New URL']
			self[old] = new
			
	def __setitem__ (self, key, value):
		if self.data.has_key(key):
			if self.strict:
				raise KeyError, "dupicate key (%s)" % key
			else:
				print"dupicate key (%s)" % key
		self.data[key] = value
		
	def __getitem__ (self, key):
		if not (self.data.has_key(key)):
			return None
		return self.data[key]
		
	def keys (self):
		sorted = self.keys()
		sorted.sort()
		return sorted
		
	def getMapping (self, url):
		return self[url]
			
def testerFoo ():
	mappings = BPPBMappings()
	print 'table has %d entries' % len(mappings)
	
	from ncar_lib.repository.reporter import Reporter
	reporter = Reporter ('/Users/ostwald/devel/python/python-lib/ncar_lib/repository/reporter/bppb.properties')
	for result in reporter.results:
		url = result.url
		mapping = mappings[url]
		if not mapping:
			print url
		# print "\n%s\n\t%s" % (url, mapping)
		
def tester ():
	mappings = BPPBMappings()
	print 'table has %d entries' % len(mappings)
	
	from tabdelimited import TabDelimitedFile
	report = TabDelimitedFile ()
	report.read('/Users/ostwald/devel/python/python-lib/ncar_lib/repository/reporter/bppb-reporter-output.txt')
	for record in report:
		url = record['url']
		mapping = mappings[url]
		if not mapping:
			print record['recId'], url
		# print "\n%s\n\t%s" % (url, mapping)
		
if __name__ == '__main__':
	tester()
	
	
