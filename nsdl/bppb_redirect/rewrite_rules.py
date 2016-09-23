import os, sys, urlparse
from tabdelimited import TabDelimitedFile, TabDelimitedRecord

# use this variable to skip any new URLs that have bogus chars
bogusUrls = []

class URL:

	def __init__ (self, urlStr):
		self.urlStr = urlStr
		parse = urlparse.urlparse(urlStr)
		self.scheme = parse[0]
		self.path = parse[2]
		self.query = parse[4]
		self.host = parse[1] # parse.hostname
		
	def __repr__ (self):
		"""
		DONT encode - we want to catch encoding errors
		"""
		# return self.urlStr.encode('utf-8')
		return self.urlStr
	
class RedirectMapping (TabDelimitedRecord):
	"""
	input is two URLs, old and new
	
	able to produce an apache rewrite rule to redirect the old to the new
	"""
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.oldUrl = URL(self['Old URL'])
		self.newUrl = URL(self['New URL'])

	def getRewriteRule (self):
		"""
		consists of a condition and a rule: e.g.
		RewriteCond %{QUERY_STRING} date=March2008&departmentid=professional
		RewriteRule ^/issue/column.php http://beyondpenguins.ehe.osu.edu/a-sense-of-place/identifying-similarities-and-difference\
s [R=permanent]

		NOTEs: 
			1 - Do not include RewriteCond if oldUrl has no query!
			2 - if there is no newURL.query, append a ? to newURL ...

		Flags: 
			L - this the LAST rule to be processed - the rest are skipped
			R=permanent - redirect with 'permanent' code
		"""
		
		flags = ['R=permanent','L']
		
		if not self.newUrl.scheme in ['http', 'https', 'ftp']:
			raise Exception, 'Illegal scheme: "%s"' % self.newUrl.scheme
		
		if str(self.oldUrl) in bogusUrls:
			raise Exception, 'newUrl has utf8 chars (oldUrl is %s)' % self.oldUrl
			
		# if there is no newURL.query, append a ? to newURL
		newUrlStr = self.newUrl.urlStr
		if not self.newUrl.query:
			newUrlStr += '?'
			
		condition = None
		if self.oldUrl.query:
			condition = 'RewriteCond %%{QUERY_STRING} %s' % self.oldUrl.query
		rewrite = 'RewriteRule ^%s %s [%s]' % (self.oldUrl.path, newUrlStr, ','.join(flags))
		
		if condition is None:
			return rewrite
		else:
			return '%s\n%s' % (condition, rewrite)
			
	def __cmp__ (self, other):
		"""
		rules are sorted from specific to general
		we only worry about the oldURL components, since these are what is matched
		first compare query (if present), then the path
		"""
		
		mine = self.oldUrl
		others = other.oldUrl
		
		if mine.query and others.query:
			val = cmp(mine.query, others.query)
			if val != 0:
				return -val # we want more specific to come FIRST
		elif mine.query:
			return -1
		elif others.query:
			return 1
			
		# neither had a query - compare the paths (not sure this is
		# very robust, since paths can contain regular expressions!
		# still, put in reverse lex order to simulate more specific paths first
		
		return -cmp(mine.path, others.path)
		
class RedirectTable (TabDelimitedFile):
	
	encoding = 'ISO-8859-1'
	# encoding = 'utf-8'
	verbose = 1
	
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=RedirectMapping)
		self.read (path)
		self.uniquePaths = self.getUniquePaths()
		self.uniqueHosts = self.getUniqueHosts()
		self.errors = []
		
	def getUniquePaths (self):
		"""
		collect the unique Old URL paths
		"""
		paths = []
		for item in self.data:
			if not item.oldUrl.path in paths:
				paths.append(item.oldUrl.path)
		return paths
		
	def getUniqueHosts (self):
		"""
		collect the unique Old URL paths
		"""
		hosts = []
		for item in self.data:
			if not item.oldUrl.host in hosts:
				hosts.append(item.oldUrl.host)
		return hosts
		
	def report (self):
		print '\n unique paths'
		for path in self.uniquePaths:
			print path
	
		print '\n unique hosts'
		for host in self.uniqueHosts:
			print host
			
	def getRules (self, host=None):
		if host:
			mappings = filter (lambda x:x.oldUrl.host==host, self.data)
		else:
			mappings = self.data
		## rules = map (lambda x:x.getRewriteRule(), mappings)
		rules = []
		for i, item in enumerate(mappings):
			try:
				rules.append (item.getRewriteRule())
			except Exception, exc:
				# print 'couldnt process item %d' % i
				self.errors.append( 'couldnt process item %d (%s)' % (i, exc))
		return '\n\n'.join (rules)
		
	def showErrors (self):
		print "\nErrors (%d)" % len(self.errors)
		for err in self.errors:
			print "- %s" % err
			
	def writeRules (self, host=None, path='RULES.txt'):
		fp = open(path, 'w')
		fp.write (self.getRules(host=host))
		fp.close()
		print ("wrote rules to %s" % path)
			
def testRewriteRule (mapping):
	"""
	mapping is an item held by table (e.g., table[0])
	"""
	print 'oldUrl.path: %s' % mapping.oldUrl.path
	print 'oldUrl.query: %s' % mapping.oldUrl.query
	print 'newUrl: %s' % mapping.newUrl
	print '\n%s\n' % mapping.getRewriteRule()	
	
def findBogusNewUrls():
	errors = []
	for item in table:
		try:
			print item.newUrl
		except Exception, exc:
			errors.append ("bog newUrl for %s\n\t%s" % (item.oldUrl, exc))
	print "\nErrors (%d)" % len(errors)
	for err in errors:
		print "- %s" % err		
	
if __name__ == '__main__':
	path = '/home/ostwald/Documents/NSDL/BPPB_Redirects/Final_Redirect_Table.txt'
	# path = '/home/ostwald/Documents/NSDL/BPPB_Redirects/TEST_Table.txt'
	table = RedirectTable(path)
	table.sort()
	if 1:
		host = 'beyondpenguins.nsdl.org'
		rules_file = 'beyondpenguins.rules'
		table.writeRules(host, rules_file)
		
	if 0:
		table.sort()
		for item in table:
			print '\n%s' % item.getRewriteRule()

	


