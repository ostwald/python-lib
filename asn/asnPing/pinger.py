"""
periodically ping various asn services, keeping the following information
url, responseTime, ...

the pinger will be run as a cron job and append it's results to a tab-delimited data file
"""
import urllib, sys, time, os
from JloXml import XmlRecord

class MyUrlOpener (urllib.FancyURLopener):
	"""
	don't raise error on 303 (redirect)
	"""
	def http_error_default(self, url, fp, errcode, errmsg, headers):
		"""Default error handler: close the connection and raise IOError."""
		void = fp.read()
		fp.close()
		if errcode != 302:
			raise IOError, ('http error', errcode, errmsg, headers)
		
## 		if errcode == 444:
## 			raise IOError, ('http error', errcode, errmsg, headers)


## 	def http_error_404(self, url, fp, errcode, errmsg, headers, data=None):
## 		"""Error 303 -- also relocated (essentially identical to 302)."""
## 		print "ERROR 404 yall"
## 		return self.http_error_default(url, fp, errcode, errmsg, headers)

class ResponseError:

	def __init__ (self, info):
		# print "RESPONSE_ERROR: %s (%s)" % (info, type(info))
		# print "!! %s !!" % info[1]
		self.name = info[0]
		try:
			self.errcode = info[1]
		except:
			self.errcode = "???"
		try:
			self.errmsg = info[2]
		except:
			self.errmsg = "???"

	def __repr__ (self):
		return "%s (%s)" % (self.errcode, self.errmsg)

class Response:

	url_opener = MyUrlOpener()	# create URLopener
	# url_opener = urllib.URLopener()	# create URLopener

	def __init__ (self,url):
		self.request = url
		self.error = None
		self.data = None
		self.clicks = time.time()
		try:
			self.data = self.url_opener.open(url).read()
		except:
			if 1:
				self.error = ResponseError (sys.exc_info()[1])
			else:
				exc_info=sys.exc_info()
				print exc_info[0], exc_info[1]
		self.clicks = time.time() - self.clicks

class Pinger:

	errcode = None
	clicks = None
	url = None
	notes = ""

	def __init__ (self, url):
		self.url = url
		response = Response (url)
		if response.error:
			# print 'ERROR: %s' % response.error
			self.errcode = response.error.errcode
		self.clicks = response.clicks

	def _timestamp (self):
		fmt = "%m/%d/%Y %H:%M:%S"
		return time.strftime (fmt, time.localtime())
		
	def report (self):
		"""
		columns: timestamp, url, clicks, errcode, notes
		"""
		s=[];add=s.append
		add (self._timestamp())
		add (self.url)
		if self.clicks:
			add ("%0.3f" % self.clicks)
		else: add ("")
		
		add ("%s" % (self.errcode or ""))
		add ("%s" % self.notes)
		# return [self.url, self.responseCode, self.clicks]
		return '\t'.join (s)

class PingManager:

	# urls to ping each time PingManager is invoked
	urls = [
		'http://purl.org/ASN/resources/S1046B24', # a resource
		'http://purl.org/ASN/scheme/ASNEducationLevel/9', # scheme (grade level)
		'http://purl.org/ASN/scheme/ASNJurisdiction/NV', # scheme jurisiction (author)
		'http://purl.org/ASN/scheme/ASNTopic/civics' , # scheme topic
		]

	def __init__ (self, path):
		if not os.path.exists (path):
			fp = open(path, 'w')
			columns = ['timestamp', 'url', 'clicks', 'errcode', 'notes']
			fp.write ('\t'.join (columns))
			fp.write('\n')
			fp.close()
		fp = open (path, 'a')
		for url in self.urls:
			fp.write (Pinger (url).report())
			fp.write ('\n')
		fp.close()
		

def pingTest ():
	# url = "http://www.dlese.org/aa"
	urls = [
		'http://purl.org/ASN/resources/S1046B24', # a resource
		'http://purl.org/ASN/resourcesX/S1046B24', # a 404
		'http://purl.orgCC/ASN/resources/S1046B24', # a address not found
		]


	for url in urls:
		print Pinger (url).report()
		
if __name__ == '__main__':
	path = "AsnPingResults.txt"
	pm = PingManager (path)
