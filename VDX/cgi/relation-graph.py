#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# above path is for purg.local

import cgi, sys, os, socket
import cgitb; cgitb.enable()

hostname = socket.gethostname()

if hostname == 'dls-rs1':
	# ccs
	sys.path.append ('/home/ostwald/python/python-lib')
	sys.path.append ('/home/ostwald/python/site-packages')
elif hostname == 'purg.local':
	sys.path.append('/Users/ostwald/devel/python/python-lib')
	sys.path.append('/Users/ostwald/devel/python/python-site-packages/')
elif hostname.startswith('iis-executor'):
	sys.path.append('/Users/ostwald/devel/python-lib')
	sys.path.append('/home/ostwald/python/site-packages/')
	print "YES"
else:
	raise Exception, "host name not recognized: %s" % hostname
import igraph



# X
# sys.path.append('/Library/WebServer/CGI-Executables/python-lib')


from VDX import LayoutVdxRecord
from VDX.bio import getEcoServiceGraphData

from HyperText.HTML import *

form = cgi.FieldStorage()

def validateRequest():
	if not 'section' in form:
		raise KeyError, "section is required" 
	if not 'teacher' in form:
		raise KeyError, "teacher is required"
	# for now require group param
	if not 'group' in form:
		raise KeyError, "group is required"

def createVdxRecord ():
	
	try:
		validateRequest()
	except KeyError, msg:
		# handle error
		# print "Content-type: text/html\n"
		raise Exception, "Request error: %s" % msg
		# return
	

	# now we grab the VDX for the request
	params = {
		'section' : form['section'].value,
		'teacher' : form['teacher'].value,
		'group' : form['group'].value,
		'command' : 'data',
		'data_type' : 'all'
	}
	
	# default is SPRING 2015 service. After that, url is sent in request as dataServiceUrl
	SPRING_2015_SERVICE_URL = 'https://script.google.com/macros/s/AKfycbxD52hA0DrPrfxfCJiqOYGyKSD3oQK8qtkUemX9THMjuSfpMe_F/exec'
	
	baseUrl = 'dataServiceUrl' in form and form['dataServiceUrl'].value or SPRING_2015_SERVICE_URL

	try:
		graphData = getEcoServiceGraphData(params, baseUrl)
		if not graphData:
			raise Exception, "no graph data"
	except Exception, msg:
		raise Exception, 'getEcoServiceGraphData ERROR: %s' % msg
	
	
	try:
		return LayoutVdxRecord(graphData)
	except Exception, e:
		raise Exception, 'Could not compute VDX: %s' % e

if __name__ == '__main__':
	try:
		resp = createVdxRecord ()
		print "Content-type: text/xml\n"
		print resp
		
	except Exception, msg:
		print "Content-type: text/html\n"
	
		print "error: %s" % msg

