import re
from JloXml import XmlRecord, XmlUtils

rec = XmlRecord(path="cmp-docs/doc2.xml")
rec.xpath_delimiter = "/"

def singleNodeTester ():
	path = 'record/contributors/person[1]/@order'
	node = rec.selectSingleNode (rec.dom, path)
	if node:
		if node.nodeType == node.ATTRIBUTE_NODE:
			print "Attribute value: " + node.nodeValue
		else:
			print node.toxml()
	else:
		print 'node not found at', path

def selectNodesTester ():
	path = 'record/contributors/person'
	nodes = rec.selectNodes (rec.dom, path)
	
	if nodes:
		print '%d nodes found at %s' % (len(nodes), path)
		for node in nodes:
			if node.nodeType == node.ATTRIBUTE_NODE:
				print "Attribute value: " + node.nodeValue
			else:
				print node.toxml()
	else:
		print 'nodes not found at', path
		
def utilsSingleNodeTester ():
	root = rec.selectSingleNode (rec.dom, 'record/contributors')
	path = 'person/@order'
	node = XmlUtils.selectSingleNode (root, path)
	if node:
		if node.nodeType == node.ATTRIBUTE_NODE:
			print "Attribute value: " + node.nodeValue
		else:
			print node.toxml()
	else:
		print 'node not found at', path
		
def utilsSelectNodesTester ():
	root = rec.selectSingleNode (rec.dom, 'record/contributors')
	path = 'person'
	nodes = XmlUtils.selectNodes (root, path)
	
	if nodes:
		print '%d nodes found at %s' % (len(nodes), path)
		for node in nodes:
			if node.nodeType == node.ATTRIBUTE_NODE:
				print "Attribute value: " + node.nodeValue
			else:
				print node.toxml()
	else:
		print 'nodes not found at', path
		
def getTextAtPathTester ():
	if 0:
		rec.xpath_delimiter = '/'
		# print rec.getTextAtPath ("/record/contributors/person[1]/lastName")
		print rec.getTextAtPath ("record/general/recordID")
	else:
		rec.xpath_delimiter = ':'
		# print rec.getTextAtPath ("record:contributors:person[1]:lastName")
		print rec.getTextAtPath ("record:general:recordID")
		
# selectNodesTester()
# singleNodeTester()
# utilsSingleNodeTester()
# utilsSelectNodesTester()
getTextAtPathTester()
