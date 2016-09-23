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
import sys, os, site
import string
import time

if (sys.platform == 'win32'):
	sys.path.append ("H:\\python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

import urllib
from urlparse import urlsplit, urljoin
from cgi import parse_qs
from JloXml import XmlRecord
from HyperText.HTML40 import *

def showArgs ():
	for i in range(len (sys.argv)):
		print "arg[%d]: %s" % (i, sys.argv[i])
	print ("\n")

class ServiceRequest:
	def __init__ (self, baseUrl, params):
		self.baseUrl = baseUrl
		self.params = params
		self.url = "%s?%s" % (baseUrl, urllib.urlencode (params))
		self.urlTuple = urlsplit(self.url)

	def getContextName (self):
		path = self.urlTuple[2]
		return path.split("/")[1]

	def getQuery (self):
		return self.urlTuple[3]

	def getParams (self):
		return parse_qs (self.getQuery())

	def display (self, indent=""):
		s=[];add=s.append

		add ("baseUrl: %s" % self.baseUrl)
		add ("contextName: %s" % self.getContextName())

		add ("params:")
		params = self.getParams()
		for p in params.keys():
			val = params[p]
			if len (val) > 1:
				add ("\t%s:" % p)
				for v in val:
					add ("\t\t%s" % v)
			else:
				add ("\t%s: %s" % (p, val[0]))

		return indent + string.join (s, "\n" + indent)
		
class ServiceClient:
	
	mail_sender = 'ostwald@comcast.net'
	mail_recipients = ['jonathanostwald@comcast.net',]
	url_opener = urllib.URLopener()	# create URLopener

	emailEnabled = 1
	verbose = 0

	def __init__ (self, baseUrl):
		self.baseUrl = baseUrl
		self.request = None
		self.success = 0

	def _getResponse (self):
		"""
		submit service request and return a DOM containing response from service

		returns None in case of http error, but we can do better ... 
		"""
		url = self.request.url
		try:
			data = self.url_opener.open(url)
		except IOError, error_code :		# catch the error
			if error_code[0] == "http error" :
				print "error_code ", error_code
				return None, error_code				
		except:
			print "error", sys.exc_type, sys.exc_value
			return None, [sys.exc_type, sys.exc_value]

		xml = data.read()
		rec = XmlRecord (xml=xml)
		return rec, None

	def mailResult (self, subject, text):
		
		# Import smtplib for the actual sending function
		import smtplib

		# Import the email modules we'll need
		from email.MIMEText import MIMEText

		me = self.mail_sender
		you = self.mail_recipients
		msg = MIMEText(text)

		# me == the sender's email address
		# you == the recipient's email address
		msg['Subject'] = subject
		msg['From'] = me
		msg['To'] = string.join (you, ", ")

		if self.emailEnabled:

			# Send the message via our own SMTP server, but don't include the
			# envelope header.
			try:
				s = smtplib.SMTP()
				s.connect()
				s.sendmail(me, you, msg.as_string())
				s.close()
			except:
				print "*** email message could not be sent!\n\t%s: %s\n" % \
					  (sys.exc_type, sys.exc_value)
		else:
			print "*** email disabled - no message sent!\n"
			
		if not self.success:
			print "self.success: %d" % self.success
			print "%s\n\n%s" % (subject, text)


class ExportCollectionClient (ServiceClient):

	def doExport (self, params):
		"""
		perform the export and then either
		- print out a string (this must be handled by crontab entry
		or
		- email message

		exmple of crontab call:
		  /home/ostwald/bin/dcs-export schemedit serceet | /bin/mail -s \
		  'Automatic DCS export of serceet' ostwald@ucar.edu 
		"""
		self.request = ServiceRequest (self.baseUrl, params)
		dom, error = self._getResponse ()
		if (dom):
			subject, msg = self._parseResponse(dom)
		else:
			self.success = 0
			if type(error) == type([]) and len(error) > 1:
				msg = "Export failed with http error code: %s\n" % error[1]
			else:
				msg = "Export failed: %s\n" % error
			msg += "\nService Request Details:\n%s\n" % self.request.display ("  ")
			
			subject = "Export Failed"

		# self.mailResult (subject, msg)
		timeStr = time.strftime("%a, %d %b %Y %H:%M%p", time.localtime(time.time()))
		print "%s at %s\n" % (subject, timeStr)
		print msg

	def _parseResponse (self, rec):
		"""
		returns (subject, msg) response
		
		look for "DCSWebService/ExportCollection/result"
		"""
		element = rec.selectSingleNode (rec.dom,"DCSWebService:ExportCollection:result")
		if element and rec.getText(element) == "Success":
			self.success = 1
			# construct success mesage
			subject = "DCS Export Service successfully initiated"
			msg = self._getSuccessMsg (rec)
			
		else:
			self.success =0
			subject = "DCS Export Service failed to initiate"
			msg = self._getFailureMsg (rec)

		return subject, msg

	def _getFailureMsg (self, rec):
		"""
		parse the failure response and create a message
		"""
		s = [];add=s.append

		errorElement = rec.selectSingleNode (rec.dom, "DCSWebService:error")
		if errorElement:
			add (rec.getText(errorElement))
			errors = rec.selectNodes (errorElement, "err")
			if errors:
				for err in errors:
					add (rec.getText(err))
			else:
				add ("no error details found")
		else:
			add ("no error information not found")

		add ("\nService Request Details:\n%s" % self.request.display ("  "))
		
		# tack on some debugging info
		if self.verbose:
			add ("\n%s\n%s" % ("-"*70, rec.dom.toxml()))

		return string.join (s, "\n")

	def _getSuccessMsg (self, rec):
		"""
		parse the failure response and create a message
		"""
		s = [];add=s.append

		successElement = rec.selectSingleNode (rec.dom,"DCSWebService:ExportCollection")
		resultUriElement = rec.selectSingleNode (successElement, "reportUri")
		if resultUriElement:
			reportUri = rec.getText (resultUriElement)
			add ("see %s" % (Href (reportUri, "detailed export report")))

		add ("\nService Request Details:\n%s" % self.request.display ("  "))
		
		# tack on some debugging info
		if self.verbose:
			add ("\n%s\n%s" % ("-"*70, rec.dom.toxml()))

		return string.join (s, "\n")

def tester ():
	collection = 'serceet'
	exportDir = 'foot'
	baseUrl = "http://128.117.126.8:8688/schemedit/services/dcsws1-0"
	params = (
		('verb','ExportCollection'),
		('collection', collection),
		('exportDir', exportDir),
		('statuses', 'Unknown'),
		('statuses', 'Final Status'),)
	client = ExportCollectionClient (baseUrl)
	client.doExport (params)
	
if __name__ == "__main__":

	tester()

					   

		

	
