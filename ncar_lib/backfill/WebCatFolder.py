"""
WebCatFolder - 

Subclasses WebCatFolder metadata and adds extra info from the WebCat node representing the folder, which contains other
helpful information, including "title" and "tn_issue" attributes.

Writes XML representation to disk.
"""
import os, sys, re, traceback
from JloXml import XmlUtils, XmlRecord
from ncar_lib.webcat_scrape.WebCatMetadata import WebCatMetadata
from ncar_lib.webcat_scrape.WebCat import WebCat
from ncar_lib.lib import webcatUtils

class WebCatFolder (WebCatMetadata):
	
	def __init__ (self, url, folderNode=None):
		self.title = None
		self.tn_issue = None
		self.node = folderNode
		if self.node:
			self.title = self.node.title
			self.tn_issue = webcatUtils.getTN(self.node.parent.title)
		WebCatMetadata.__init__ (self, url)

	def finalizeXml (self):
		"""
		doctor the metadata with information contained in the folderNode
		"""
		if not self.node:
			return
			
		# get TN issue from title, or if not from parent's title
		self.tn_issue = self.getTN() or self.tn_issue
		if self.tn_issue:
			print "ADDING %s" % self.tn_issue
			tnElement = XmlUtils.addElement (self.dom, self.doc, "tn_isssue")
			XmlUtils.setText(tnElement,  self.tn_issue)
			self.title = webcatUtils.stripIssue (self.title, self.tn_issue)
			self.setFieldValue ("title", self.title)
			
		childrenElement = XmlUtils.addElement (self.dom, self.doc, "children")
		for child in self.node.children:
			# XmlUtils.addChild  (self.dom, "child", child.title, childrenElement)
			
			md = child.getMetadata(None)
			id = md.getAccessionNum ()
			print id
			childElement = XmlUtils.addChild  (self.dom, "child", child.title, childrenElement)
			childElement.setAttribute ("accessionNum", id);
		children = XmlUtils.getChildElements (self.doc)
		self.doc.appendChild (childrenElement)
		

		
	def write (self, filename, dir="."):
		doPP = True
		path = os.path.join (dir, filename + ".xml")
		if os.path.exists (path):
			msg = "Could not write: File already exists for %s" % path
			raise Exception,  msg
		## XmlRecord.write(self, path)
		if doPP:
			fp = open (path, 'w')
			fp.write (self.__repr__())
			fp.close()
		else:
			XmlRecord.write(self, path)
		print 'wrote %s' % os.path.basename(path)
		
	def getTN (self):
		return webcatUtils.getTN(self.title)
	
def tester():
	url = "http://library.ucar.edu/uhtbin/cgisirsi/LGhbpxS0Qh/SIRSI/100580013/511/6919"
	folder = WebCatFolder (url)
	print folder
	
if __name__ == '__main__':
	title = "NCAR/TN-21+EDD - Balloon stress-band analysis"
	issue = webcatUtils.getTN (title)
	print stripIssue (title, issue)

