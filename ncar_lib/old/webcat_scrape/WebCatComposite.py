"""
WebCatComposite - a metadata record holding information about "leaf" 
WebCatMetadata records
"""
import os, sys, traceback
from JloXml import XmlUtils, XmlRecord
from WebCatMetadata import WebCatMetadata

class WebCatComposite (WebCatMetadata):
	
	def __init__ (self, url, compNode=None):
		self.node = compNode
		WebCatMetadata.__init__ (self, url)
	
	def finalizeXml (self):
		if not self.node:
			return
		childrenElement = XmlUtils.addElement (self.dom, self.doc, "children")
		for child in self.node.children:
			XmlUtils.addChild  (self.dom, "child", child.title, childrenElement)
		
		children = XmlUtils.getChildElements (self.doc)
		self.doc.appendChild (childrenElement)
		
	def write (self, filename, dir="."):
		path = os.path.join (dir, filename + ".xml")
		if os.path.exists (path):
			msg = "Could not write: File already exists for %s" % path
			raise Exception,  msg
		XmlRecord.write(self, path)
		
def processCompositeRecords (url, collection):
	from WebCat import WebCat
	
	destDir = "WebCatCompositeData/%s" % collection
	if not os.path.exists (destDir):
		os.makedirs(destDir)
	
	cat = WebCat (url)
	node = cat.getNode (collection)
	composites = cat.getComposites (node)
	for comp in composites:
		print comp.title
	count = len (composites)
	errors = []
	for i, comp in enumerate (composites):
		try:
			url = comp.metadatapath
			md = WebCatComposite (url, comp)
			# print md
			md.write(str(i), destDir)
			msg = "%d/%d" % (i, count)
			print (msg)
		except:
			errors.append ( "%d/%d: couldn't write: %s" % (i, count, sys.exc_info()[1]))
			# traceback.print_tb (sys.exc_info()[2])
	if errors:
		print "\nERRORS:\n" + "\n".join (errors)
		
def wcCompositeTest ():
	url = "http://www.library.ucar.edu/uhtbin/cgisirsi/Oi7yYgz8ku/SIRSI/310750009/511/6926"
	wcComp = WebCatComposite (url)
	print wcComp
	
def process ():
	url = "http://www.library.ucar.edu/uhtbin/cgisirsi/LB6aIUfpqc/SIRSI/264390009/503/995"
	collection = "NCAR Manuscripts"
	processCompositeRecords (url, collection)
if __name__ == '__main__':
	# wcCompositeTest ()
	process()
