"""
utils for handling data written by excel
"""

import os, sys, re, codecs
from JloXml import RegExUtils


verbose = 0
# data_linesep = '\n\r' # windows
# data_linesep = '\r' # mac
data_linesep = '\n' # unix

ingest_data_dir = '/home/ostwald/Documents/NSDL/Backpack/ingest/ingest-data'
# html_data_encoding = 'ISO-8859-1' # "utf-8"
html_data_encoding = 'utf-8' # "utf-8"

def getHtml (path, encoding=None, linesep=None):
	linesep = linesep or data_linesep
	myEncoding = encoding or html_data_encoding
	print 'getHtml() encoding: %s' % myEncoding
	print '  path:', path
	html = codecs.open(path,'r',myEncoding).read()
	# html = open(path,'r').read()

	lines = html.split(linesep)
	if verbose:
		print '%d lines read' % len(lines)
		if linesep == '\r':
			print 'spliting on mac NL'
	html = u'\n'.join(lines)
	return html

		

condPat = re.compile('<!\[if[\s]+.*?<!\[endif\]>', re.DOTALL)
hrefPat = RegExUtils.attrPattern ("href")
tagPat = re.compile ('<([^\s^/^<]+)[\s]*?[^<]*?>', re.DOTALL) # matches opening tag (e.g., '<table ...>'
htmlCommentPat = re.compile ('<!--.*?-->', re.DOTALL)
	
def xcelHtml2Xml (html):
	"""
	clean up the html so it can be processed as XML.
	this involves stripping attributes, which often are not quoted
	"""
	clean = ""
	i = 0
	while i<len(html):
		ch = html[i]

		m = condPat.match (html, i)
		if m:
			i = m.end()
			continue
			
		m = htmlCommentPat.match (html, i)
		if m:
			i = m.end()
			continue
		
		m = tagPat.match(html, i)
		if m:
			# print "%s (end=%d)" % (m.group(), m.end())
			tag = m.group(1)
			# print 'tag: "%s"' % tag
			
			# if the tag is 'a', we don't want to blow the href attribute away ...
			if tag == 'a':
				hm = hrefPat.search (m.group())
				if hm:
					clean += '<a href="%s">' % hm.group(1)
				else:
					raise Exception, 'href attribute not found in %s' % m.group()
				# clean += '%s' % m.group(0)
			elif tag in ['col']:  # blow these away completely
				pass
			else:
				clean += '<%s>' % m.group(1)
			i = m.end()
			continue
			
		clean += ch
		i = i+1
	# <br> will choke xml parsers!
	clean = clean.replace ('<br>','')
	return clean
	
if __name__ == '__main__':
	pass
