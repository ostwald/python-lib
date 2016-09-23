import sys, re
from serviceclient import SimpleClient
from JloXml import RegExUtils as rexml




h2Tag_pat = rexml.getTagPattern ('h2')
attr_pat = rexml.attrPattern('name')
a_pat = rexml.getTagPattern('a')

def get_modules(url):

	client = SimpleClient (url)

	html = client.getData()

	m = h2Tag_pat.findall(html)

	modules = []
	
	if 0 and m:
		print 'm is TRUE'
		print ' there are %d in m' % len(m)
		print 'the first element is a %s' % type (m[0])

	if not m:
		return []
	for s in m:
		m2 = attr_pat.match (s)
		if not m2:
			# print 'could not find name attribute in "%s"' % s
			continue
		m3 = a_pat.match(s)
		if not m3:
			# print 'could not match on a tag'
			continue

		modules.append(m3.group(1))
	return modules

def report_modules(url):
	print url
   	modules = get_modules(local_url)
	for m in modules:
		print ' -- %s' % m

def searchTester():
	m =  h2Tag_pat.search(html)
	if m:
		print m.group(0)
		
if __name__ == '__main__':
	urls = {
		'localhost' : 'http://localhost/phpinfo.php',
		'osws' : 'https://osws.ucar.edu/phpinfo.php'
		}
	for url in urls:
		local_url = 'http://localhost/phpinfo.php'
		report_modules(local_url)
