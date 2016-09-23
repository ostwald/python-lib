import urllib
import re
from JloXml import RegExUtils

webcatDomain = "http://library.ucar.edu"

def pp (node):
	raw = node.toprettyxml ("  ","\n")
	s = [];add=s.append
	for line in raw.split('\n'):
		if line.strip():
			add (line)
	return '\n'.join (s)

class WebCatLink:

	def __init__ (self, tuple):
		self.label = tuple[1].strip()
		self.url = webcatDomain + "/" + tuple[0].strip()

	def __repr__ (self):
		return '%s: %s' % (self.label, self.url)

# Archive Browse Page - contains links to pages that display 20 Technical notes at a tile
def getArchiveBrowsePage ():
	url = "http://library.ucar.edu/uhtbin/cgisirsi/sYfxPvBlCW/SIRSI/106300008/503/993"
	filename = "archiveBrowsePage.html"
	data = urllib.URLopener().open(url)
	content = data.read()
	fp = open(filename, 'w')
	fp.write (content)
	fp.close()
	print "wrote to ", filename

def stripComments (html):
	pat = re.compile ("<!--.*?-->", re.S)
	return pat.sub ("", html)

def getIndexLinkPat (matchtext):
	textPat = "[\s]*%s[\s]*[\d]+-[\d]+" % matchtext
	return re.compile ("<A HREF=\"([\S]+?)\">(" + textPat + ")</A>", re.DOTALL)	
	
def getIndexLinks (matchtext, content):
	"""
	grab the links to the index pages (that display links 20 Tech notes at a time)
	"""
	# finds all links with textual content
	## pat = re.compile ("<A HREF=\"[\S]+?\">[^<]+?</A>", re.DOTALL) 

	pat = getIndexLinkPat (matchtext)
	results = re.findall (pat, content)
	return results

def stripAttributes (content, tags):
	if type(tags) == type(""):
		tags = [tags]
	for tag in tags:
		pat = re.compile ("<" + tag + "[^>]*?>", re.DOTALL)
		m = pat.search (content)
		if m:
			print "found: ", m.group()
		else:
			print "not found"
		content = pat.sub ("<"+tag+">", content)
	return content

def removeBoldTags (content):
	content = content.replace ("<B>", "")
	content = content.replace ("</B>", "")
	return content
	
def removeFontTags (content):
	out = ""
	i = 0
	# tag = "FONT"
	# patStr = "<%s.*?>(.*?)</%s>" % (tag, tag)
	# tagPat = re.compile (patStr, re.DOTALL)
	tagPat = RegExUtils.getTagPattern ("FONT")
	while i < len(content):
		m = tagPat.match (content[i:])
		if not m:
			out = out + content[i]
			i = i + 1
			continue
		out = out + m.group(1)
		i = i + m.end()
	return out

	
def fixAttributes (content):
	out = ""
	i = 0
	tagPat = re.compile ("<([A-Za-z]+)([^>]*?)>", re.DOTALL)
	while i < len(content):
		m = tagPat.match (content[i:])
		if not m:
			out = out + content[i]
			i = i + 1
			continue
		tag = m.group(1).strip()
		attrs = m.group(2).strip()
		attrs = normalizeAttributes (attrs)
		out = out + "<%s" % tag
		if attrs:
			out = out + " " + attrs
		if tag == "IMG":
			out = out + "/"
		out = out + ">"
		i = i + m.end()
	return out
	
def normalizeAttributes (attStr):
	normalized = []
	for attr in attStr.split(" "):
		if not attr:
			continue
		splits = attr.split("=")
		name = splits[0]
		if not name.strip():
			continue
		try:
			val = splits[1].strip()
		except:
			continue
		if not val:
			continue
		if val[0] in ["'", '"']:
			val = val[1:-1]
		normalized.append ('%s="%s"' % (name, val))
	return " ".join(normalized)

def fixImgTags (content):
	pass
	
def getLinks (matchtext, content):
	"""
	grab the links to the index pages (that display links 20 Tech notes at a time)
	"""
	# finds all links with textual content
	## pat = re.compile ("<A HREF=\"[\S]+?\">[^<]+?</A>", re.DOTALL) 

	textPat = "[\s]*%s[\s]*" % matchtext
	pat = re.compile ("<A HREF=\"([\S]+?)\">(" + textPat + ")</A>", re.DOTALL)
	results = re.findall (pat, content)
	return results
	
def getLink (matchtext, content):
	links = getLinks (matchtext, content)
	if len(links) != 1:
		print len (links), " links found"
		msg = "Link Not Found for %s" % matchtext
		raise Exception, msg
	return WebCatLink(links[0])

def getIndexItems (content):
	links = getIndexLinks ('NCAR Technical Notes', content)
	print '%d links found' % len(links)
	items = []
	for l in links:
		items.append (WebCatLink(l))
	return items
		
def someTester ():
	content = open ("archiveBrowsePage.html").read()
	items = getIndexItems(content)
	for item in items:
		print item	
		
if __name__ == "__main__":
	foo = """<TD NOWRAP ALIGN="left" VALIGN="center"
      COLSPAN=900>
	  <FONT SIZE=2><b>hello</b></FONT>"""
	print removeFontTags (foo)

