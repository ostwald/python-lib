"""
get osmRecord from disk
"""
import os, sys, re, time
from ncar_lib import OsmRecord
from JloXml import DcsDataRecord

import ncar_lib
ncar_lib_dir = os.path.dirname (ncar_lib.__file__)
data_dir = os.path.join (ncar_lib_dir, 'dups', 'data-5-17')
osmDir = os.path.join (data_dir, 'metadata')
dscDataDir = os.path.join (data_dir, 'dcs_data')

prefixMap = {
	'PUBS-NOT-FY2010' : 'not-fy10',
	'OSGC' : 'osgc',
	'PUBS' : 'pubs-ref',
	'AMS-PUBS' : 'ams-pubs',
	'NAB' : 'ncar-books'
	}

prefixPat = re.compile ('(.*?)-000.*')

def getPrefix (recId):
	m = prefixPat.match (recId)
	if not m:
		raise Exception, 'prefix not found (%s)' % recId
	return m.group(1)
	
def getCollectionKey (recId):
	"""
	from the provided recId, first obtain the prefix and using the prefix get the collectionKey
	"""
	prefix = getPrefix(recId)
	return prefixMap[prefix]
	
def getTitleKey (title):
	"""
	cast title to lower case and then remove all non-alphas
	"""
	s = ""
	for ch in title.lower():
		if ord(ch) >= 97 and ord(ch) <= 122:
			s = s + ch
	return s
	
def getTimeStamp(timeStr):
	"""
	return time in seconds for provided timeStr (e.g., 2010-09-20T14:44:13Z)
	"""

	format = '%Y-%m-%dT%H:%M:%SZ'
	tple = time.strptime(timeStr, format)
	return time.mktime(tple)
	
def getPrettyTimeStr (timeStr):
	"""
	return time in seconds for provided timeStr (e.g., 2010-09-20T14:44:13Z)
	"""

	uglyformat = '%Y-%m-%dT%H:%M:%SZ'
	tple = time.strptime(timeStr, uglyformat)
	prettyformat = "%m/%d/%Y %H:%M"
	return time.strftime(prettyformat, tple)
	
def getDiskRecord (recId):
	collectionKey = prefixMap[getPrefix(recId)]
	path = os.path.join (osmDir, collectionKey, recId+'.xml')
	return OsmRecord(path=path)
	
def getDiskDcsDataRecord (recId):
	collectionKey = prefixMap[getPrefix(recId)]
	path = os.path.join (dscDataDir, collectionKey, recId+'.xml')
	return DcsDataRecord(path=path)
	
# ----------- dcs_data stuff ------------------	
	
def getDcsStatus (recId):
	rec = getDiskDcsDataRecord (myid)
	print "%s - %s" % (rec.getStatus(), rec.getChangeDate())
	
def cleanStatusNotes (recId):
	rec = getDiskDcsDataRecord (myid)
	for entry in rec.entryList:
		entry.set('statusNote', 'fooberry')
		print entry
	
if __name__ == '__main__':
	timeStr = '2010-09-20T14:44:13Z'
	print getPrettyTimeStr (timeStr)
	print getDiskRecord ('PUBS-NOT-FY2010-000-000-000-006')

	
