"""
	FileTools - classes to support working with the various files
	associated with a DcsInstance
"""

import sys, os, site, string
if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")
					 
from PathTool import localize
from JloXml import XmlRecord
from dcsTools.instanceWalker import InstanceWalker, DcsInstance

class FileTool (XmlRecord):
	def __init__ (self, instance):
		self.instance = instance
				
class ServerXmlTool (XmlRecord):

	def __init__ (self, instance):
		self.instance = instance
		XmlRecord.__init__ (self, path=instance._get_server_xml_path())
	
	def _get_param (self, element, paramName):
		"""
		extracts an parameter element with an attribute "name" equal to
		"paramName" from the given element.

		e.g., used to extract a certain parameter from a context element
		"""
		params = self.getElementsByXpath (element, "Parameter")
		for p in params:
			a = p.getAttribute("name")
			if a == paramName:
				return p
		
	def _get_context (self, pathName):
		"""
		gets the context element with a "path" attribute having the value held
		by "pathName".

		e.g., for DCS instances on bolide, the pathName will be the instance name
		"""
		context_xpath = "Service:Engine:Host:Context"

		contexts = self.getElementsByXpath (self.doc, context_xpath)
		# print  "%d context paths found" % len(contexts)

		for c in contexts:
			a = c.getAttribute ("path")
			if a == "/"+pathName: 
				return c

	def getContextParam (self, paramName):
		context = self._get_context (self.instance.name)
		param = None
		if context:
			param = self._get_param (context, paramName)
		if param:
			return param.getAttribute ("value")
		
	def getExportBaseDir (self):
		return self.getContextParam ("exportBaseDir")

	def getCatalogingInfo (self):
		return self.getContextParam ("catalogingInfo")

	def getInfo (self):
		s=[];add=s.append
		add ("%s" % self.instance.name)
		add ("exportBaseDir: %s" % self.getExportBaseDir())
		add ("catalogingInfo: %s" % self.getCatalogingInfo())
		return string.join (s, "\n\t")

## - a ServerXMLTool application --------------
def serverXmlTester (instance):
	tool = ServerXmlTool (instance)
	print tool.recordXml
	context = tool._get_context ("schemedit")
	if context:
		exportBaseDir = tool._get_param (context, "exportBaseDir")
	print exportBaseDir.getAttribute("value")
		
## - FrameworkConfigTool --------------	
	
class FrameworkConfigTool (XmlRecord):

	fieldInfoURI_path = "frameworkConfigRecord:editorInfo:fieldInfoURI"
	
	def __init__ (self, instance, xmlFormat):
		self.instance = instance
		self.xmlFormat = xmlFormat
		path = instance._get_framework_config_path (xmlFormat + ".xml")
		# if not os.path.exists (path):
			# raise IOError, "file not found "
		XmlRecord.__init__ (self, path=path)
		
	def getFieldInfoURI (self):
		return self.getTextAtPath (self.fieldInfoURI_path)
		
	def updateFieldInfoURI (self):
		newFileName = "fields-list"
		fieldInfoURI = self.getFieldInfoURI()
		if not fieldInfoURI:
			print "fieldInfoURI not found in " + self.path
			return
		if fieldInfoURI.find (newFileName) != -1:
			print "file already updated for '%s'" % self.xmlFormat
			return
		newFieldInfoURI = fieldInfoURI.replace ("filename-list", newFileName)
		print "\n\told: %s\n\tnew: %s" % (fieldInfoURI, newFieldInfoURI)
		self.setTextAtPath (self.fieldInfoURI_path, newFieldInfoURI)
		
	def rename (self, newName):
		dst = localize (os.path.join (os.path.dirname (self.path), newName))
		os.rename (self.path, dst)
		if (os.path.exists (dst)):
			self.path = dst	
			print "framework_config file renamed as " + dst
		else:
			raise IOError, "framework_config file apparently not renamed to " + dst
		
## -------------------------------------------------------------
##
##  FrameworkConfigTool applications
##
			
def update_framework_config_files(baseDir):	
	InstanceWalker (baseDir).walk (update_configs)

def delete_framework_config_files(baseDir):	
	InstanceWalker (baseDir).walk (delete_configs)
	
def update_configs (instance):
	writeToDisk = 1
	print "%s\nUpdating %s\n" % ("-"*50, string.upper (instance.name))
	xmlFormats = [
		'adn',
		'dlese_anno',
		'news_opps',
		'dlese_collect',
		]
	for xmlFormat in xmlFormats:
		tool = FrameworkConfigTool (instance, xmlFormat)
		print xmlFormat
		tool.updateFieldInfoURI()
		if writeToDisk:
			tool.write()
		else:
			print "\t\t .........  file not written to disk"
		
def delete_configs (instance):
	print "%s\nDeleting configs for %s\n" % ("-"*50, string.upper (instance.name))
	xmlFormats = [
		'adn',
		'dlese_anno',
		'news_opps',
		'dlese_collect',
		]
	for xmlFormat in xmlFormats:
		try:
			tool = FrameworkConfigTool (instance, xmlFormat)
		except IOError:
			print sys.exc_value
			print "\tcontinuing ...."
			continue
		path = tool.path
		tool.delete_file()
		if os.path.exists (path):
			print "file NOT deleted at " + path
		else:
			print "%s.xml deleted" % xmlFormat
		
## --------------------------------------------------------
	
	
if __name__ == "__main__":
	## instancepath = localize ("L:/ostwald/tomcat/tomcat")
	instancepath = localize ("/export/services/dcs/dcs.dlese.org/tomcat/roles")
	instance = DcsInstance (instancepath)
	# delete_configs (instance)

	# baseDir = localize ("L:\\ostwald\\tomcat")
	baseDir = localize ("/export/services/dcs/dcs.dlese.org/tomcat")
	delete_framework_config_files(baseDir)






