#!/usr/bin/env python

import sys, os, site

if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

from PathTool import localize
from string import join
import urllib
from glob import glob

class DcsInstance:
	def __init__ (self, path, displayname=None):
		self.path = path
		self.name = os.path.basename (path)
		self.displayname = displayname
		if not self.displayname:
			self.displayname = self.name

	def toString (self):
		s=[];add=s.append
		add ("Instance: %s" % self.name)
		add ("\t%s" % self.path)
		return join (s, "\n")

	def showMe (self):
		print self.toString()

	def _get_webapps_dir (self):
		return os.path.join (self.path, "webapps")

	def _get_server_xml_path (self):
		return os.path.join (self.path, "conf","server.xml")
		
	def _get_framework_config_dir_path (self):
		return os.path.join (self.path, "dcs_conf", "framework_config")
		
	def _get_framework_config_path (self, xmlFormat):
		return os.path.join (self._get_framework_config_dir_path(), xmlFormat)
		
	def isInstance (self):
		"""
		the following must be true:
		- path must be a directory
		- path must not be a link
		- must contain a "webapps" subdirectory
		"""
		return os.path.isdir (self.path) and \
			   not os.path.islink(self.path) and \
			   os.path.exists (self._get_webapps_dir())

class InstanceWalker:
	"""
	navigates a directory of tomcat instances
	"""
	host = os.getenv("HOST")
	requiredHost = None # "bolide"
	## baseDir = "/export/services/dcs/dcs.dlese.org/tomcat"
	configPath = ""
	fixerClass = ""

	def __init__ (self, baseDir):

		if self.requiredHost and self.host != self.requiredHost:
			msg =  "Instance walker must be instantianted on %s" % self.requiredHost
			raise "InitError", msg
		if not os.path.exists (baseDir):
			msg =  "baseDir does not exit at %s" % baseDir
			raise "InitError", msg
		self.baseDir = baseDir
		## print "Instance Walker instantiated at %s" % baseDir
		self.instances = self._get_instances()
		self.instanceNames = self._get_instanceNames()

	def getInstance (self, instanceName):
		for i in self.instances:
			if i.name == instanceName:
				return i

	def _get_instances (self):
		"""
		return list of instances sorted by instance.name
		"""
		instances = []
		for filename in os.listdir (self.baseDir):
			i = DcsInstance(os.path.join (self.baseDir, filename))
			if i.isInstance():
				instances.append(i)
		instances.sort (lambda a, b: cmp(a.name, b.name))
		return instances

	def _get_instanceNames (self):
		return map (lambda i:getattr(i, "name"), self.instances)

	def walk (self, fn):
		"""
		call supplied function on each instance. NOTE: supplied function takes
		an DcsInstance object as a param
		"""
		if len (self.instances) == 0:
			print "... no Dcs Instances found!"
		else:
			for i in self.instances:
				fn(i)

def walker_test ():
	## baseDir = "/export/services/dcs/dcs.dlese.org/tomcat"
	## baseDir = "L:\\ostwald\\tomcat"
	if (sys.platform == 'win32'):
		baseDir = "L:/ostwald/tomcat"
	else:
		baseDir = "/devel/ostwald/tomcat"
	try:
		walker = InstanceWalker (baseDir)
	except:
		print sys.exc_type, sys.exc_value
	walker.walk (lambda i:i.showMe())

def walker_test2():	
	baseDir = localize ("L:\\ostwald\\tomcat")
	try:
		walker = InstanceWalker (baseDir)
	except:
		print sys.exc_type, sys.exc_value
	walker.walk (lambda i:getExportBaseDir(i))

def getInstanceTest (instanceName):
	baseDir = "L:\\ostwald\\tomcat"
	try:
		walker = InstanceWalker (baseDir)
	except:
		print sys.exc_type, sys.exc_value
	instance = walker.getInstance(instanceName)
	instance.showMe()
	
	
def getExportBaseDir (instance):
	from fileTools import ServerXmlTool
	s = ServerXmlTool (instance)
	print "\n%s" % instance.name
	context = s._get_context ("schemedit")
	if context:
		exportBaseDir = s._get_param (context, "exportBaseDir")
		print "\t%s" % exportBaseDir.getAttribute("value")
	else:
		print "\texportBase not found"

	
def instance_test ():
	path = "L:/ostwald/tomcat/tomcat"
	instancePath = localize(path)
	i = DcsInstance (instancepath)
	if i.isInstance():
		print i.toString()
	else:
		print "not an instance"

if __name__ == "__main__":

	walker_test2()
	# getInstanceTest("tomcatx")







