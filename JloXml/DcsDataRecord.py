from xml.dom.minidom import parse, parseString
from xml.parsers.expat import ExpatError
from XmlUtils import getText, getChildText, setText, getChild
import sys
import string
import os
import re
import codecs
import time

from JloXml import MetaDataRecord

class DcsDataRecord (MetaDataRecord):

	id_path = "dcsDataRecord:recordID"
	lastTouchDate_path = "dcsDataRecord:lastTouchDate"
	lastEditor_path = "dcsDataRecord:lastEditor"
	ndrInfo_path = "dcsDataRecord:ndrInfo"
	ndrHandle_path = ndrInfo_path + ":ndrHandle"
	ndrLastSyncDate_path = ndrInfo_path + ":lastSyncDate"	
	
	def __init__ (self, path=None, xml=None):
		"""
		exposes entryList, an ordered list of statusElement objects
		"""
		MetaDataRecord.__init__ (self, path, xml)
		self.updateEntryList () # initializes self.entryList
		self.entriesElement = self.selectSingleNode (self.doc, "statusEntries")


	def makeNdrInfo (self, ndrHandle=None):
		if self.getNdrInfo():
			raise DOMException, "ndrInfo already exists"
		ndrInfo = self.addElement (self.doc, "ndrInfo")
		handle = self.addElement (ndrInfo, "ndrHandle")
		if ndrHandle:
			self.setText (handle,ndrHandle)
		lastSync = self.addElement (ndrInfo, "lastSyncDate")
		self.setText (lastSync, self.getLastTouchDate())
		self.addElement (ndrInfo, "syncError")
		return ndrInfo
		
	def getNdrInfo (self):
		return self.selectSingleNode (self.dom, self.ndrHandle_path)
		
	def getNdrHandle (self):
		return self.getTextAtPath (self.ndrHandle_path)	
		
	def setNdrHandle (self, ndrHandle):
		self.setTextAtPath (self.ndrHandle_path, ndrHandle)
		
	def getLastSyncDate (self):
		return self.getTextAtPath (self.ndrLastSyncDate_path)	
		
	def setLastSyncDate (self, lastSyncDate):
		self.setTextAtPath (self.ndrLastSyncDate_path, lastSyncDate)
		
	def getLastTouchDate (self):
		return self.getTextAtPath (self.lastTouchDate_path)

	def setLastTouchDate (self, val):
		self.setTextAtPath (self.lastTouchDate_path, val)
		
	def getLastEditor (self):
		return self.getTextAtPath (self.lastEditor_path)

	def setLastEditor (self, val):
		self.setTextAtPath (self.lastEditor_path, val)
		
	def updateEntryList (self):
		self.entryList = self.get_sortedEntryList()
		
	def getStatusFlag (self):
		"""
		returns status of most recent entry
		"""
		self.get_sortedEntryList()
		if self.entryList:
			return self.entryList[0].status
			
	def getStatus (self):
		"""
		returns "Done" if the flag is a finalStatus
		"""
		flag = self.getStatusFlag()
		if flag is None:
			return None
		return flag.startswith("_|-final-") and "Done" or flag
	
	def getStatusNote (self):
		"""
		returns status of most recent entry
		"""
		self.get_sortedEntryList()
		if self.entryList:
			return self.entryList[0].statusNote
			
	def getChangeDate (self):
		"""
		returns status of most recent entry
		"""
		self.get_sortedEntryList()
		if self.entryList:
			return self.entryList[0].changeDate
			
	def getId (self):
		return self.getTextAtPath (self.id_path)
		
	def setId (self, newId):
		self.setTextAtPath (self.id_path, newId)

	def get_sortedEntryList (self):
		"""
		return sorted list of StatusElement instances
		"""
		status_entries = []
		entries = self.selectNodes (self.doc, "statusEntries:statusEntry")
		# print ("get_statusEntryList: %d entries found" % len (entries))
		for element in entries:
			# entry = StatusEntry (element.toxml())
			entry = StatusElement (element)
			status_entries.append (entry)
		status_entries.sort (self.statusEntryCmp)
		return status_entries 

	## move bulk of this code to statusEntry??
	def addStatusEntry (self, **args):
		entriesElement = self.entriesElement
		if not entriesElement:
			raise "entries element element not found"

		statusEntry = self.dom.createElement("statusEntry")
		for key in args.keys():
			element = self.dom.createElement(key)
			text = self.dom.createTextNode (args[key])
			element.appendChild (text)
			statusEntry.appendChild (element)
		self.entriesElement.appendChild (statusEntry)
		self.updateEntryList ()
		return statusEntry

	def set_defaults (self, id):
		defaults = {
			"recordID":id,
			"lastTouchDate":utils.datestamp(),
			}
		self.update (defaults)
		
	def getCurrentStatusEntry (self):
		if self.entryList:
			return self.entryList[0]

	def statusEntryCmp (self, s1, s2):
		d1 = s1.timeStamp
		d2 = s2.timeStamp
		if d1 < d2: return 1
		if d1 > d2: return -1
		return 0

	def showEntryList (self):
		s=[];add=s.append
		add ("\nSorted Entry List")
		for entry in self.entryList:
			add (str(entry))
		print (string.join (s, "\n\n"))

class StatusElement:

	"""
	Works on a Status entry as an element
	"""
	
	def __init__ (self, element):
		self.element = element
		attrs = ("changeDate", "status", "statusNote", "editor")
		for attr in attrs:
			setattr (self, attr, self.get(attr))
		self.timeStamp = self._get_timeStamp()

	def _get_timeStamp (self):
		timestamp_fmt = "%Y-%m-%dT%H:%M:%SZ"
		## print "changeDate: ", self.changeDate
		time_tuple = time.strptime (self.changeDate, timestamp_fmt)
		return time.mktime(time_tuple)
		
	def get (self, tag):
		return getChildText (self.element, tag)
		
	def set (self, tag, value):
		child = getChild (tag, self.element)
		if child:
			setText (child, value)
		

	def __repr__ (self):
		s=[];add=s.append
		attrs = ("changeDate", "status", "statusNote", "editor")
		for attr in attrs:
			add ("%s: %s" % (attr, self.get(attr)))
		return string.join (s, "\n")

class StatusEntry:

	"""
	not yet tested or debugged!
	
	we might want to subclass Element for status entry ...
	"""
	
	def __init__ (self, xml):
		self.xml = xml
		attrs = ("changeDate", "status", "statusNote", "editor")
		for attr in attrs:
			setattr (self, attr, self.get(attr))
		self.timeStamp = self._get_timeStamp()


	def _tag_pattern (self, tag):
		str = "<%s>(?P<content>.*?)</%s>" % (tag, tag)
		return re.compile (str, re.DOTALL)

	def _get_timeStamp (self):
		timestamp_fmt = "%Y-%m-%dT%H:%M:%SZ"
		## print "changeDate: ", self.changeDate
		time_tuple = time.strptime (self.changeDate, timestamp_fmt)
		return time.mktime(time_tuple)

	def getTagContent (self, tag):
		p = self._tag_pattern (tag)
		m = p.search (self.xml)
		if m:
			return m.group("content")
		
	def get (self, tag):
		return self.getTagContent (tag)

	def __repr__ (self):
		s=[];add=s.append
		attrs = ("changeDate", "status", "statusNote", "editor")
		for attr in attrs:
			add ("%s: %s" % (attr, self.get(attr)))
		return string.join (s, "\n")

def convert_time (timestr):
	"""
	converts the time stamps found in the logs to other representations
	"""
	# timestamp_fmt = "%b %d, %Y %I:%M:%S %p"
	timestamp_fmt = "%Y-%m-%dT%H:%M:%SZ"
	time_tuple = time.strptime (timestr, timestamp_fmt)   # a tuple representing the timestr
	secs = time.mktime(time_tuple)

	## print "time_tuple", time_tuple
	## print "secs", secs
	## print "asci", time.asctime (time_tuple)

def tester():
	if sys.platform == 'win32':
		path = "H:/tmp/dcsDataRecord.xml"
	else:
		path = "/home/ostwald/tmp/dcsDataRecord.xml"
	rec = DcsDataRecord (path)
	print "\nid: ", rec.getId()
	entries = rec.entryList
	print "\n%d entries found" % len (entries)
	cs = rec.getCurrentStatusEntry ()
	print "\nCurrent Entry:"
	if cs:
		print "%s" % cs
	else:
		print "\tnothing found"
	rec.showEntryList()

if __name__ == "__main__":

##	tester()
	path = "/dls/devel/ostwald/records/dcs_data/dlese_collect/collect/DCS-COLLECTION-000-000-000-010.xml"
	rec = DcsDataRecord (path)
	print rec.getId()
	rec.setId ("asssssssss");
	print rec.getId()
