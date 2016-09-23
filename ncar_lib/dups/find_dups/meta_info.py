"""
use lastTouchData to determine which records have been recently modified
"""
import os, time, sys, re
from UserList import UserList
from JloXml import XmlRecord, XmlUtils
from ncar_lib.dups.utils import getDiskRecord, getCollectionKey, getTimeStamp
from ncar_lib.time_date_utils import unionDateToSecs

class RecordInfo:
	
	def __init__ (self, element):
		self.element = element
		self.recId = self.element.getAttribute ("recId")
		self.lastTouch = self.element.getAttribute ("lastTouch")
		self.timeStamp = getTimeStamp(self.lastTouch)
		self.pubsId = self.element.getAttribute ("pubsId")
		self.status = self.element.getAttribute ("status")
		self.collection = getCollectionKey(self.recId)
		
		
	def set (self, attr, value):
		self.element.setAttribute(attr, value)
		setattr(self, attr, value)
		
	def getRecord (self):
		return getDiskRecord (self.recId)
		
	def __cmp__ (self, other):
		return cmp(self.timeStamp, other.timeStamp)
		
	def __repr__ (self):
		return "%s (%s) - %s (%s)" % (self.lastTouch, self.pubsId, self.recId, self.status)

class CollectionInfo(UserList):
	
	# baseDir = "meta-metadata"
	baseDir = '/home/ostwald/python-lib/ncar_lib/dups/data/meta-metadata'
	
	def __init__ (self, collection):
		UserList.__init__ (self)
		self.collection = collection
		self.dataPath = os.path.join (self.baseDir, collection+'.xml')
		print "DATA_PATH: ", self.dataPath
		self.rec = XmlRecord (path=self.dataPath)
		nodes = self.rec.selectNodes (self.rec.dom, "collectionInfo:rec")
		print "%d recs read from meta-metadata" % len(nodes)
		map (self.append, map(RecordInfo, nodes))
		
	def selectByUnionDate (self, unionDate):
		"""
		takes union date (e.g., 2011, 2011-02, 2011-02-25)
		and returns recs having lastTouch AFTER union date
		"""
		threshold = unionDateToSecs (unionDate)
		predicate = lambda x:x.timeStamp >= threshold
		return self.select (predicate)

	def select (self, predicate):
		"""
		applies predicate to each item
		returns only those for which preciate is True
		"""
		return filter (predicate, self.data)
		
	def write (self, path=None):
		"""
		self.rec writes to self.rec.path by default
		"""
		self.rec.write(path)
		
if __name__ == '__main__':
	collections = ['osgc', 'pubs-ref', 'not-fy10']
	col = 'pubs-ref'
	colInfo = CollectionInfo (col)
	recs = colInfo.select("2011")
	for rec in recs:
		print rec
	print "-----\n%d recs found" % len (recs)
