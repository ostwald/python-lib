"""
we have a situation in which there are framework configuration files that have
lost the namespaceinfo from the root element. we need a script to find these
files and replace the namespaceinfo

this is what the root element should look like:
  <collectionConfigRecord
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="file:/services/dcs/dcs.dlese.org/tomcat/<INSTANCE>/webapps/schemedit/WEB-INF/metadata-frameworks/collection-config/dcsCollectionConfig.xsd">
"""

import os
import sys
import string
import re

class NameSpaceFixer:

	schemaUri = None
	rootElementName = None
	xmlns = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'

	def __init__ (self, path):
		self.path = path
		self.xml = open (self.path, 'r').read()
		self.schemaLoc = self.getSchemaLoc()
		self.filename = os.path.basename(self.path)
		self.rootElementPat = self.getRootElementPat()
		self.nameSpaceInfo = self.getNewNameSpaceInfo()

	def getNewNameSpaceInfo (self, instance=None):
		return 	"%s %s" % (self.xmlns, self.schemaLoc)

	def getFileNameSpaceInfo (self):

		m = self.rootElementPat.search (self.xml)
		if m:
			return string.strip(m.group(1))
		else:
			return None

	def hasNameSpaceInfo (self):
		info = self.getFileNameSpaceInfo ()
		return  info != None and info != ""

	def getRootElement (self):
		m = self.rootElementPat.search (self.xml)
		if m:
			return string.strip(m.group())
		else:
			return None

	def getRootElementPat (self):
		return  re.compile ("<%s[\s]*(.*?)>" % self.rootElementName, re.DOTALL)

	def getSchemaLoc (self):
		return 'xsi:noNamespaceSchemaLocation="%s"' % self.schemaUri

	def replaceNameSpaceInfo (self):
		existing = self.getRootElement()
		new = "<%s %s>" % (self.rootElementName, self.nameSpaceInfo)
		return re.sub (existing, new, self.xml)


class CollectionNameSpaceFixer (NameSpaceFixer):

	schemaUri = "http://www.dpc.ucar.edu/people/ostwald/Metadata/framework-config/dcsFrameworkConfig-0.0.3.xsd"
	rootElementName = "collectionConfigRecord"

	def __init__ (self, path, instance=None):
		self.instance = instance
		NameSpaceFixer.__init__ (self, path)

	def getSchemaLoc (self):
		if self.instance is None:
			return NameSpaceFixer.getSchemaLoc (self)
		else:
			loc = "/dpc/services/dcs/dcs.dlese.org/tomcat/%s/webapps/schemedit/WEB-INF/metadata-frameworks/collection-config/dcsCollectionConfig.xsd" % self.instance
			return 'xsi:noNamespaceSchemaLocation="%s"' % loc

class FrameworkNameSpaceFixer (NameSpaceFixer):

	schemaUri = "http://www.dpc.ucar.edu/people/ostwald/Metadata/framework-config/dcsFrameworkConfig-0.0.3.xsd"
	rootElementName = "frameworkConfigRecord"

if __name__ == "__main__":
	baseDir = "L:\\ostwald\\python\\namespace"
	good_path = os.path.join (baseDir, "collection-config-good.xml")
	bad_path = os.path.join (baseDir, "collection-config-bad.xml")

	f = CollectionNameSpaceFixer(good_path, "FOOBERRY")
	print "\n%s\nold root element \n%s" % (50*'_', f.getRootElement())
	print "\n%s\nnew record \n%s" % (50*'_', f.replaceNameSpaceInfo())


