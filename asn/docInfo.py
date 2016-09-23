"""
DocInfo - data structures to hold summary info from StdDocument instances used to make table of contents 
(toc) for browser.
"""

import os, sys
from util import makeKey
from HyperText.HTML40 import *
from JloXml import XmlUtils, XmlRecord
from HtmlDocument import MyDocument

coloInfo = {
'author':'Colorado',
'topic' :'science',
'filename' : 'Science-1995-Colorado-Content Standards for Science.xml',
'title' : 'Colorado Model Content Standards for Science',
'description' : 'The Colorado model standards presented here specify what all students should know and be able to do in science as a result of their school studies. Specific expectations are given for students completing grades K-4, 5-8, and 9-12. These standards reflect high expectations and outline the essential level of science knowledge and skills needed by all citizens to participate productively in our increasingly technological society. Some suggestions are also offered for those students who elect to extend their study of science beyond that specified in these content standards, based on their particular interests, motivation, career goals, and needs.',
'version' : 'http://purl.org/ASN/export/1.4.1',
'fileCreated' : 'Mar 13 2008',
'created' : '1995',
'docId' : '??'
}

nsesInfo = {
'author' :'NSES',
'topic' : 'science',
'filename': 'Science-1995-Colorado-Content Standards for Science.xml',
'title' : 'National Science Education Standards',
'description' : None,
'version' : 'http://purl.org/ASN/export/1.4.1',
'fileCreated' : 'Mar 13 2008',
'created' : '1995',
'docId' : '??'
}

class DocInfo:
	
	attrs = ['author', 'topic', 'filename', 'title', 'description',  
			'version', 'fileCreated', 'created', 'docId']
	
	def __init__ (self, stdDoc):
		
		if hasattr (stdDoc, "path"):
			self.path = stdDoc.path
		else:
			self.path = "unknown"
		for attr in self.attrs:
			setattr (self, attr, getattr (stdDoc, attr))
			
	def toMap (self):
		map = {}
		for attr in self.attrs:
			map [attr] = getattr (self, attr)
		return map
		
	def asElement (self):
		doc = XmlUtils.createDocument ("docInfo")
		root = doc.documentElement
		root.setAttribute ("path", self.path)
		for attr in self.attrs:
			val = getattr (self, attr) or ""
			# print "%s: %s" % (attr, val)
			XmlUtils.addChild (doc, attr, val)
		element = doc.removeChild (root)
		doc.unlink()
		return element
		
	def __repr__(self):
		s=[];add=s.append
		add (makeKey (self))
		for attr in self.attrs:
			add ("\t%s: %s" % (attr, getattr (self, attr)))
		return '\n'.join  (s)

class XmlDocInfo (DocInfo):
	"""
	create a DocInfo instance from an XML element
	"""
	def __init__ (self, element):
		self.path = element.getAttribute ("path")
		for attr in self.attrs:
			val = XmlUtils.getChildText (element, attr).strip()
			setattr (self, attr, val)
		
class TestDocInfo (DocInfo):
	"""
	create a DocInfo instance from an map
	"""
	def __init__ (self, map):
		self.path = "unknown"
		for attr in self.attrs:
			setattr (self, attr, map[attr])
			
def docInfoTester ():
	docInfo = TestDocInfo (nsesInfo)
	print docInfo.asElement().toprettyxml()

	
if __name__ == '__main__':
	docInfoTester()

