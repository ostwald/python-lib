"""
RecordGrouper - Reads a collection-data file (e.g., 'not-fy10-records.xml') and produces
GROUPINGS (based on SortedGroupingDict), which are dicts whose values are lists
of "grouped" records. The SortedGroupingDict.getGroupingKey() method determines the
key for each record and thus does the actual grouping. For example, the TitleMap
class groups records with identical title.

The SortedGroupingDict instances write the grouped data to "grouping-data" files, named
after the concrete SortedGroupingDict class. For example, TitleMap writes a grouping-data
file as "TitleMap.xml"

"""
import os, sys, time
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils
from ncar_lib.dups.utils import getDiskRecord, getTitleKey
from ncar_lib.repository.get_record import GetRecord
from ncar_lib import unionDateToSecs

class RecordInfo:
	"""
	represents a record element in the data file (e.g., 'not-fy10-records.xml')
	
	exposes attributes (as strings):
		'recId', 'status', 'title', 'pubName', 'fiscalYear', 'titleKey'
		
	NOTE: the attributes of this class are determined by the elements in the data_file
		see "collection_data.RecInfo" or the data file itself
		
	RecordInfo instances have access to metadata and dcs_data files on disk if we need to pluck
	data from them (this is much faster than using web service, but requires that a
	copy of the metadata records are available on disk).
	"""
	def __init__ (self, element):
		self.element = element
		for attr in ['recId', 'status', 'title', 'pubName', 'fiscalYear', 'titleKey']:
			setattr (self, attr, self.element.getAttribute(attr))
			
		# self.updatePubName()
		
	def getOsmRecord (self):
		# return getDiskRecord (self.recId)
		response = GetRecord(self.recId).response
		print response.recId
		return response.payload
		
	def updatePubName (self):
		"""
		an example of how to add more info to the RecordInfo
		- the RecordGrouper instance must be written for change to persist
		"""
		osmRecord = self.getOsmRecord ()
		pubName = osmRecord.getPubName() or ""
		setattr (self, 'pubName', pubName)
		self.element.setAttribute ('pubName', pubName)
			
	def __repr__ (self):
		return '%s - %s' % (self.pubsId, self.title)
			
class SortedDict (UserDict):
	"""
	Maintains keys in sorted order
	"""
	
	def keys (self):
		"""
		keys are sorted
		"""
		sorted = self.data.keys()
		sorted.sort()
		return sorted
	
class SortedGroupingDict (SortedDict):
	"""
	abstract base class for grouping maps
	"""
	def getGroupingKey (self, recInfo):
		"""
		produces the grouping key for provided recInfo
		"""
		raise Exception, 'getKey not implemented'
		
	def getReportingKeys (self, threshold=2):
		"""
		returns keys of items to report.
		usually we only want to report groups that have a certain
		minimum number of members.
		- threshold - min members required to include
		"""
		dupKeys = []
		for key in self.keys():
			if len(self[key]) >= threshold:
				dupKeys.append(key)
		return dupKeys
		
	def addItem (self, recInfo):
		"""
		add a recInfo instance to this map
		"""
		key = self.getGroupingKey(recInfo)
		if key in self.data.keys():
			vals = self[key]
		else:
			vals = []
		vals.append (recInfo)
		self[key] = vals
		
	def toxml (self, path=None):
		"""
		write this map as xml to a file in the "grouping_data" directory, named after the classname
		"""
		if path is None:
			path = 'grouping_data/' + self.__class__.__name__ + '.xml'
		rec = XmlRecord (xml="<dupGroups/>")
		rec.doc.setAttribute ('name', self.__class__.__name__)
		groupNum = 1
		for key in self.getReportingKeys():
			groupEl = XmlUtils.addElement (rec.dom, rec.doc, 'group')
			groupEl.setAttribute('key', key)
			groupEl.setAttribute('size', str(len(self[key])))
			groupEl.setAttribute('groupNum', str(groupNum))
			for recInfo in self[key]:
				groupEl.appendChild (recInfo.element.cloneNode(1))
			groupNum = groupNum + 1
		rec.write(path)
		print 'wrote to ', path
		
		
class TitleMap (SortedGroupingDict):
	"""
	groups records by exact title match
	"""
	def getGroupingKey (self, recInfo):
		"""
		return record title
		"""
		return recInfo.title
		
	def report (self, threshold=1):
		print "\n---------------------------\nTitleMap"
		for title in self.keys():
			if len(self[title]) > threshold:
				print '(%d) %s' % (len(self[title]), title)

class PubsIdMap (SortedGroupingDict):
	"""
	groups records by duplicat pubsId
	"""
	
	def getGroupingKey (self, recInfo):
		"""
		return record pubsId
		"""
		return recInfo.pubsId
		
	def report (self, threshold=1):
		reportingKeys = self.getReportingKeys ()
		print "\n---------------------------\nPubsIdMap"
		for pubsId in reportingKeys:
			print '(%d) %s' % (len(self[pubsId]), pubsId)
				
class TitlePubNameMap (SortedGroupingDict):
	
	"""
	groups records by titleFrag+pubName
	"""
	
	def getGroupingKey (self, recInfo):
		"""
		(first-try) take only title before first colon,
		take all of the title before the LAST colon
		then apply getTitleKey,
		and finally append the pubName
		"""
		# titleFrag = recInfo.title.split(':')[0]  # too many titles had multiple colons ...
		splits = recInfo.title.split(':')
		if len(splits) > 1:
			titleFrag = ':'.join (splits[:-1])
		else:
			titleFrag = recInfo.title
		return getTitleKey(titleFrag) + '_' + recInfo.pubName
		
	def report (self, threshold=1):
		reportingKeys = self.getReportingKeys ()
		print "\n---------------------------\nTitlePubNameGroup"
		for pubsId in reportingKeys:
			print '(%d) %s' % (len(self[pubsId]), pubsId)
			
class TitleGroupingMap (SortedGroupingDict):

	"""
	groups records by key constructed by "flattening" title
	"""
	
	def getGroupingKey (self, recInfo):
		"""
		return a key contstructed from the title
		"""
		return getTitleKey(recInfo.title)
	
	def report (self, threshold=1):
		reportKeys = self.getReportingKeys()
		print "\n---------------------------\nTitleGroupingMap (%d groups)" % len(reportKeys)
		for key in reportKeys:
			print '\n(%d) %s' % (len(self[key]), key)
			for recInfo in self[key]:
				print ' %s - %s (%s)' % (recInfo.title, recInfo.recId, recInfo.pubsId)
		
	def asTabDelimited (self, path):
		fields = [ 'title', 'recId','fiscalDate', 'status']
		lines = [];add=lines.append
		hdr = '\t'.join(fields + ['dup group'])
		add (hdr)
		i = 1
		for key in self.getReportingKeys():
			for recInfo in self[key]:
				add ('\t'.join (map (lambda x:getattr(recInfo, x), fields) + [str(i)]))
			i = i + 1
		content = '\n'.join (lines)
		fp = open(path, 'w')
		fp.write(content)
		fp.close()
		print 'wrote to', path

		
class RecordDataReader (SortedDict):
	"""
	Reads the data in the collection-data file	
	"""
			
	data_path = 'not-fy10-records.xml'

	def __init__ (self, acceptFn=None):
		self.acceptFn = acceptFn is None and self.acceptAll or acceptFn
		self.read()
		
	def read (self):
		self.data = {}
		self.data_rec = XmlRecord (path=self.data_path)
		self.data_rec.xpath_delimiter = "/"
		recNodes = self.data_rec.selectNodes (self.data_rec.dom, 'not-fy10-records/record')
		print '%d records read' % len(recNodes)
		i = 0
		for recNode in recNodes:
			recInfo = RecordInfo (recNode)
			i = i + 1
			if i % 500 == 0:
				print "%d/%d" % (i, len(recNodes))
				
			if not self.acceptFn (recInfo):
				continue
			self.addRecord (recInfo)		
			
	def acceptAll (self, recInfo):
		return 1
			
	def acceptFy0809OFF (self, recInfo):
		"""
		accept only records with fiscalYear of 2008 or 2009
		"""
		return recInfo.fiscalYear in ['2008', '2009']
			
	def addRecord (self, recInfo):
		self[recInfo.recId] = recInfo		
					
class RecordGrouper (RecordDataReader):
	"""
	reads a DATA FILE (at data_path) containing information about all records in not-fy10 collection, e.g.,
	    <record fiscalDate="1990-07-23" 
		    pubName="Conference on Cloud Physics" 
			pubsId="101009" recId="PUBS-NOT-FY2010-000-000-000-001" 
			status="Unknown" 
			title="Precipitation development in Colorado front range snowstorms: 15 November 1987 Case study"/>
			
		the data file is produced by title_dups.NotFy10RecordsSearcher
		
	traverses records, ignoring those not accepted by "acceptFn" (e.g., acceptFy0809)
	
	calls "addRecord" for each accepted record, which populates the various xxxMaps (which
		are all instances of SortedGroupingDict). The maps have a "toxml()" method, which write
		their contents to an xml file (
	
	"""
			
	data_path = 'not-fy10-records.xml'
	
	groupings = [
		# 'titleMap',
		'titleGroupingMap',
		'titlePubNameMap'
		]

	def __init__ (self, acceptFn=None):
		if 'titleMap' in self.groupings:
			self.titleMap = TitleMap()
		if 'titleGroupingMap' in self.groupings:
			self.titleGroupingMap = TitleGroupingMap()
		if 'titlePubNameMap' in self.groupings:
			self.titlePubNameMap = TitlePubNameMap()
		RecordDataReader.__init__(self, acceptFn)
						
	def addRecord (self, recInfo):
		self[recInfo.recId] = recInfo
		
		for grouping in self.groupings:
			if hasattr(self, grouping):
				getattr(self, grouping).addItem(recInfo)
		
	def writeGroupingData (self):
		for grouping in self.groupings:
			if hasattr(self, grouping):
				getattr(self, grouping).toxml()		
			
	def write (self, path=None):
		"""
		writes the data file (e.g. to preserve data added to record elements)
		"""
		if path is None:
			path = self.data_rec.path
		self.data_rec.write(path)
		print 'wrote to ', path
			
def isFy0809 (recInfo):
	"""
	predicate accept only records with fiscalYear of 2008 or 2009
	"""
	return recInfo.fiscalYear in ['2008', '2009']
		
def processAllRecords ():
	recs = RecordGrouper()
	# recs.titleMap.report()
	# recs.titleGroupingMap.report()
	# recs.pubsIdMap.report()
	# recs.titleGroupingMap.asTabDelimited('dups-all.txt')
	# recs.write()
	# recs.titleGroupingMap.toxml()
	recs.titlePubNameMap.toxml()
	
def processFY0809Records ():
	recs = RecordGrouper(RecordGrouper.acceptFy0809)
	recs.titleMap.report()
	recs.titleGroupingMap.report()
	# recs.titleGroupingMap.asTabDelimited('dups-all.txt')
	
if __name__ == '__main__':
	# processAllRecords()
	RecordGrouper(isFy0809).writeGroupingData()

		
