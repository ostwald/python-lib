import sys, os, re
from UserDict import UserDict
from UserList import UserList

from lxml import etree as ET

__author__ = 'ostwald'

class XmlRecord:

	namespaces = {}
	xpaths = {}

	def __init__ (self, xml):
		parser = ET.XMLParser(recover=True, encoding='utf-8', remove_blank_text=True)
		try:
			self.dom = ET.fromstring(xml, parser)
		except:
			raise Exception, 'Could not parse provided xml: %s' % sys.exc_info()[1]

	def setValueAtNamedPath (self, path_name, value, context=None):
		self.setTextAtPath (self.getPath(path_name), value, context)
		if hasattr(self, path_name):
			setattr(self, path_name, value)

	def getValueAtNamedPath(self, path_name, context=None):
		return self.getTextAtPath (self.getPath(path_name), context)

	def getValuesAtNamedPath(self, path_name, context=None):
		"""
		return list of values
		"""
		nodes = self.selectNodesAtPath(self.getPath(path_name), context)
		return map(lambda x:x.text.strip(), nodes)

	def getValuesAtPath(self, path, context=None):
		nodes = self.selectNodesAtPath(path, context)
		return map(lambda x:x.text.strip(), nodes)

	def getPath(self, attr):
		return self.xpaths[attr]

	def getTextAtPath(self, path, context=None):
		nodes = self.selectNodesAtPath(path, context)
		if len(nodes):
			try:
				return nodes[0].text.strip()
			except:
				return ''
		else:
			print 'NOTHING FOUND'

	def setTextAtPath(self, path, value, context=None):

		"""
		throw exception if node is not found at path
		"""
		nodes = self.selectNodesAtPath(path, context)
		if len(nodes):
			if type(value) == type(''):
				value = unicode(value)
			nodes[0].text = value
		else:
			raise Exception, 'node not found at %s' % path

	def selectNodesAtPath(self, path, context=None):
		if context is None: context = self.dom
		nodes = context.xpath(path, namespaces=self.namespaces)
		return nodes

	def selectSingleNode(self, path, context=None):
		nodes = self.selectNodesAtPath(path, context)
		if len(nodes):
			return nodes[0]
		return None

	def selectNodeAtNamedPath(self, path_name, context=None):
		return self.selectSingleNode(self.getPath(path_name), context)

	def filterResults(self):
		pass

	def __repr__(self):
		return ET.tostring(self.dom, pretty_print=True)