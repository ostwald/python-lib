import os, sys
from util import makeKey, SortedDict
from HyperText.HTML40 import *
from JloXml import XmlUtils, XmlRecord
from HtmlDocument import MyDocument
from docInfo import XmlDocInfo
from catServiceClient.asnUriService.asnHelper import AsnHelper
			
class Toc (SortedDict):
	
	title = "ASN Science Standards Documents"
	
	def __init__ (self, docInfos=[], helper=None):
		self.helper = helper
		SortedDict.__init__ (self)
		for docInfo in docInfos:
			self.addEntry (docInfo)
	
	def addEntry (self, docInfo):
		self[makeKey (docInfo)] = docInfo
			
	def getTocHtml (self):
		toc = UL()
		for key in self.keys():
			
			# url = key + ".html"
			# inktext = "%s (%s)" % (self.helper.getAuthor(docInfo.author), docInfo.created)
			# href = Href (url, inktext,
						 # title=docInfo.title, 
						 # target="content")
			link = self.getLink (key)
			toc.append (LI (link, klass="toc-link", id=key))
		return toc
		
	def getLink (self, key):
		docInfo = self[key]
		url = key + ".html"
		inktext = "%s (%s)" % (self.helper.getAuthor(docInfo.author), docInfo.created)
		return Href (url, inktext,
					 title=docInfo.title, 
					 target="content")
		
	def asXml (self):
		## doc = XmlUtils.createDocument ("toc")
		rec = XmlRecord (xml="<toc/>")
		for docInfo in self.values():
			el = docInfo.asElement()
			rec.doc.appendChild (el)
		return rec
		
	def writeXml (self, path=None):
		path = path or "toc.xml"
		self.asXml().write(path)
		
	def toHtml (self):
		"""
		Generate the html document as string
		"""
		title = "toc"
		doc = MyDocument (title=title, stylesheet="styles.css")
		# doc.body["onload"] = "init();"
		
		# <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		
		doc.head.append (META(http_equiv="Content-Type",
                          content="text/html; charset=utf-8"))
		
		doc.addJavascript ("javascript/prototype.js")
		doc.addJavascript ("javascript/toc-scripts.js")
		doc.append (H4 (self.title, align="center"))
		
		doc.append (self.getTocHtml())
		return doc
		
	def write (self, path):
		# f = open (path, 'w')
		self.toHtml().writeto (path)

		print "toc written to ", path
			
class TopicToc (Toc):
	title = "ASN Standards Documents"
	topics = SortedDict()
	
	def addEntry (self, docInfo):
		Toc.addEntry (self, docInfo)
		topic = docInfo.topic
		if not topic in self.topics.keys():
			self.topics[topic] = []
		self.topics[topic].append(makeKey (docInfo))
		self.writeXml()
		
	def getTocHtml (self):
		html = DIV ()
		for topic in self.topics.keys():
			html.append (DIV (B (self.helper.getTopic (topic)), klass="topic-header"))
			toc = UL()
			print "topic items"
			topic_keys = self.topics[topic]
			topic_keys.sort()
			for key in topic_keys:
				
				# url = key + ".html"
				# inktext = "%s (%s)" % (self.helper.getAuthor(docInfo.author), docInfo.created)
				# href = Href (url, inktext,
							 # title=docInfo.title, 
							 # target="content")
				print "\tkey: ", key
				link = self.getLink (key)
				toc.append (LI (link, klass="toc-link", id=key))
			html.append (toc)
		return html
		
def tocTester ():
	toc = Toc ([TestDocInfo (coloInfo), TestDocInfo (nsesInfo)])
	# print toc.toHtml()
	print toc.writeXml()
	
	
def readTocXml ():
	docInfos = []
	# rec = XmlRecord ("doctored-toc.xml")
	rec = XmlRecord ("browser/toc.xml")
	## print rec
	elements = rec.doc.getElementsByTagName ("docInfo")
	## print "%d docInfos read" % len (elements)
	for element in elements:
		docInfos.append (XmlDocInfo (element))
		# print (docInfo)
	toc = TopicToc (docInfos, AsnHelper())
	print toc.toHtml()
	
if __name__ == '__main__':
	# docInfoTester()
	# tocTester()

	readTocXml()
