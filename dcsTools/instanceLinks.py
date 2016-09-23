"""
Instance Links - make a web page that provides links to certain pages in dcs
that we want to jump to. E.g.,

     Sessions Page
	 Framework_config
	 Collections Management


1 - get list of instances

2 - for each instance, make a link (or links)
    links should open up in a separate window (or frame?)
	maybe have a menu of possible pages. then provide a link
	for each instance that will call a js function to open the
	corresponding page
"""

#!/usr/bin/env python
usage = """
DCS utility script usage:
   arg0 is dcs - the command you typed to get here
   arg1 is command:
       start_jvm
       stop_jvm
       deploy
       tail
       bounce
       update
       check
       config_info
   arg2 is dcs instance name

"""
import sys, os, site, re
import string
import urllib

import sys
if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from PathTool import localize
from HyperText.HTML40 import *

from dcsTools import InstanceWalker
from dcsTools.fileTools import ServerXmlTool


class DcsInstanceLinks:

	base_url = "http://dcs.dlese.org/"
	tomcatDir = "/export/services/dcs/dcs.dlese.org/tomcat"
	## html_out_path = "H:/tmp/DCS-links.html"
	## html_out_dir = "M:/webroot/v2/dpc.ucar.edu/docroot/people/ostwald/dcs-instances"
	instances = [
		"agi",
		"argonne",
		"cat",
		"cipe",
		"dcc",
		"dpc",
		"evalcoreservices",
		"k-12community",
		"mynasadata",
		"news",
		"noaa",
		"preview",
		"roles",
		"swi",
		"tapestry",
		"unavco",
		"utig",
		]

	links = {
		"Home" : "/admin/browse.do",
		"Sessions" : "/admin/admin.do?page=sessions",
		"Collection Settings" : "/admin/admin.do?page=collections",
		}
	
	def __init__ (self):

		try:
			self.instanceWalker = self._get_instanceWalker(self.tomcatDir)
		except:
			self.instanceWalker = None

	def _get_instanceWalker (self, tomcatDir):
		try:
			walker = InstanceWalker (tomcatDir)
		except:
			msg = "WARNING: could not initialize InstanceWalker"
			print "%s\n\t(%s)" % (msg, sys.exc_value)
			# sys.exit()
		return walker

	def getInstances (self):
		if self.instanceWalker:
			return self.instanceWalker.instanceNames
		else:
			return self.instances

	def jsInstancesList (self):
		s=[];add=s.append
		for instance in self.instances:
			add ('"%s",' % instance)
		return string.join (s, "\n")
			
	def getInstanceUrl (self, name):
		return self.base_url + name


	def getLink (self, instance, link):
		url = self.getInstanceUrl (instance) + self.links[link]
		return DIV (Href (url, link, target="instance"), klass="link")


	def getLinksTable (self):
		table = TABLE (klass="instance-table", cellspacing="1")
		for name in self.getInstances():
			row = TR (klass="instance-row")
			row.append (TD (DIV (name, klass="instance-name")))
			for link_name in self.links.keys():
				row.append (TD (self.getLink (name, link_name), align="center"))
			table.append (row)
		return table.__str__()

	def renderHtmlOLD (self, html_out_dir):
		template = open (os.path.join (html_out_dir, "conrolTemplate.html"), 'r').read()
		start_tag = "<!-- begin links table -->"
		end_tag = "<!-- end links table -->"
		patString = start_tag + "(.*?)" + end_tag

		pat = re.compile (patString, re.DOTALL)
		m = pat.search (template)
		if m:
			replace = start_tag + '\n' + self.getLinksTable() + '\n' + end_tag
			return re.sub (m.group(), replace, template)
		else:
			raise "region %s NOT Found", template

	def renderHtml (self, html_out_dir):
		template = open (os.path.join (html_out_dir, "conrolTemplate.html"), 'r').read()
		start_tag = "// begin instances list"
		end_tag = "// end instances list"
		patString = start_tag + "(.*?)" + end_tag

		pat = re.compile (patString, re.DOTALL)
		m = pat.search (template)
		if m:
			replace = start_tag + '\n' + self.jsInstancesList() + '\n' + end_tag
			return re.sub (m.group(), replace, template)
		else:
			raise "region %s NOT Found", template
			
	def updatePage (self, html_out_dir):
		html = self.renderHtml(html_out_dir)
		out_path = os.path.join (html_out_dir, "control.html")
		f = open (out_path, 'w')
		f.write (html)
		f.close ()
		## print "HTML Written to %s\n\n%s" % (out_path, html)
		print "HTML Written to %s\n" % out_path

if __name__ == "__main__":
	
	html_out_dir = "/Users/ostwald/Desktop/DCSLinkTool/new/"
	# html_out_dir = localize ("H:/tmp/dcs-instances")
	DcsInstanceLinks().updatePage(html_out_dir)

