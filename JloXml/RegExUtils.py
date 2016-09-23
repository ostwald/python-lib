import re

"""
 xml utilities using regular expressions. lifted from dcc-trans/statusMaker.py
 and kept just in case they become useful at some point
"""

debug = 0

def prtln (s):
	if debug:
		print s

def getTagPattern (tag):
	"""
	finds a tag set for specified tag, and captures the content in group(1)
	- question: how does this work with nested tags?

	- useage:
	pat = getTagPattern ('div')
    m = pat.search (html)
    if m: ....

	see also: tag_contents()
	"""
	# patStr = "<%s>(.*?)</%s>" % (tag, tag) # does NOT account for attributes
	patStr = "<%s.*?>(.*?)</%s>" % (tag, tag) # DOES account for attributes
	return re.compile (patStr, re.DOTALL)
	
def getLeafTagPattern (tag):
	"""
	"<%s.*?/>" % tag
	matches elements that are self closing 
	- they can have attributes but no content
	"""
	patStr = "<%s.*?/>" % tag
	return re.compile (patStr, re.DOTALL)
	
def attrPattern (attr):
	"""
	matches the specified attribute and captures the attribute value in group(1)
	"""
	patStr = ".*?%s=\"(.*?)\".*?" % attr
	return re.compile (patStr, re.DOTALL)

def indexOf (s, tag):
	"""
	finds the first occurrence of specified tag
	returns -1 if not found
	"""
	pat = getTagPattern (tag)
	m = pat.search (s)
	if m:
		return m.start()
	else:
		return -1

def tag_contents (s, tag):
	"""
	uses getTagPattern() to extract the content of specified tag
	"""
	pat = getTagPattern (tag)
	m = pat.search (s)
	if m:
		return m.group(1)
	else:
		return None
	
# remove all leaf tags (e.g., <br />) from the given string
def _strip_leafTags (s):
	pat = re.compile ("<[^/]*/\s*>", re.DOTALL)
	while (pat.search (s)):
		s = re.sub (pat, '', s)
	return s
		
def replace_tag (s, tag, value):
	# patStr = "<%s>(.*)</%s>" % (tag, tag)
	# pat = re.compile (patStr, re.DOTALL)
	pat = getTagPattern (tag)
	m = pat.search (s)
	if m:
		prtln ("existing %s: %s" % (tag, m.group(1)))
		repl = "<%s>%s</%s>" % (tag, value, tag)
		s = re.sub (pat, repl, s)
	else:
		prtln ("%s tag not found" % tag)
	return s

def stuff (self, **args):
	"""
	insert keyword name/value pairs into record
	"""
	for key in args.keys():
		self.prtln ('%s: %s' % (key, args[key]))
		self.replace_tag (key, args[key])

def update (self, dict):
	"""
	insert dict key:value pairs into record
	"""
	for key in dict.keys():
		self.replace_tag (key, dict[key])
		
