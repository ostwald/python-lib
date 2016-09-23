"""
create a search web service explorer html page.

see example at bottom of page

"""

import os, string, sys
import re
from HyperText.HTML40 import *

if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

class Explorer:

	templateDir = "M:/webroot/v2/dpc.ucar.edu/docroot/people/ostwald/dcsws-testers"
	templatePath = os.path.join (templateDir, "DcsStatusExplorerTemplate.html")

	def __init__ (self, serverContext):
		self.html = open (self.templatePath, 'r').read()
		self.baseUrl = serverContext + '/services/ddsws1-0'
		self.collections = []
		self.statuses = []

		# print self.html

	def addCollection (self, ky, name, checked=None):
		"""
		  ky -- collection ky (as the collection is indexed)
		  name -- collection name (label for check box)
	    """
		self.collections.append (self.getCheckBox ("collection", ky, name, checked))

	def addStatus (self, status, checked=None):
		"""
		  status -- status flag LABEL
	    """
		self.statuses.append (self.getCheckBox ("dcsStatus", status, status, checked))

	def updateHtml (self):
		if self.collections:
			cText = string.join (map (str, self.collections))
			self.replaceRegion ("collection", cText)

		if self.statuses:
			sText = string.join (map (str, self.statuses))
			self.replaceRegion ("status", sText)
		
		self.replaceBaseUrl (self.baseUrl)

	def replaceBaseUrl (self, baseUrl):
		pat = re.compile ('var baseUrl = "(.*?)";')
		m = pat.search (self.html)
		if m:
			self.html = re.sub (m.group(1), baseUrl, self.html)
		else:
			print "baseUrl not found"
			print self.html

	def setPath (self, path):
		self.path = path
		dir = os.path.split (path)[0]
		if not os.path.exists (dir):
			raise "directory does not exist at %s" % dir

	def write (self):
		f = open (self.path, 'w')
		f.write (self.html)
		f.close()
		print "html written to %s" % self.path

	def replaceRegion (self, id, newtext):
		start_tag = "<!-- begin %s check boxes -->" % id
		end_tag = "<!-- end %s check boxes -->" % id
		patString = start_tag + "(.*?)" + end_tag

		pat = re.compile (patString, re.DOTALL)
		m = pat.search (self.html)
		if m:
			replace = start_tag + '\n' + newtext + '\n' + end_tag
			self.html = re.sub (m.group(), replace, self.html)
		else:
			raise "region %s NOT Found" % id

	def getCheckBox (self, name, value, prompt, checked=None):
		id = value + '_' + name
		input = INPUT (id=id, type="checkbox", name=name, value=value, checked=checked)
		label = LABEL (prompt, label_for=id)
		return DIV (input, label)

## print getCheckBox ("collection", "myCol", "myCol")

if __name__ == "__main__":
	e = None
	e = Explorer('http://dcs.dlese.org/tapestry')
	e.addCollection ('01112905194691', 'Indigenous Science', 1)
	# e.addCollection ('0o', 'Cutting Edge')
	e.addStatus ('Done')
	e.addStatus ('To DLESE')
	e.updateHtml()
	e.setPath ('m:/webroot/v2/dpc.ucar.edu/docroot/people/ostwald/dcsws-testers/tester.html')
	## e.write()
	print '%s\n\n%s' % ('_'*70, e.html)
