"""
we want to grab more info from records for which we have mapped id and lastMod times.
We walk down the rec_mods for a list of records, e.g., 
	- all records in a collection
	- records modified since a certain date,
	- etc
For each ID we extract info from the getRecord response (would it be just as well to copy these
collections to disk (physically copy the collections from tambora??)

We want to match records by PUBS ID to identify the Known duplicates.

If we want to be exhaustive, this would motivate copying files to local disk, rather than using web service


"""
import os, sys
from ncar_lib.dups.find_dups.meta_info import CollectionInfo, RecordInfo
from ncar_lib.repository import GetRecord
from ncar_lib.dups.find_dups.utils import getDiskRecord, getDiskDcsDataRecord

collectionKeys = ['osgc', 'pubs-ref', 'not-fy10']

class RecInfoExtender:
	
	dowrites = 1
	
	def __init__(self, col):
		self.col = col
		
		self.collection = CollectionInfo (self.col)
		
		maxTimes = 5000
		allRecs = self.collection.data
		maxRecs = allRecs[:maxTimes]
		since2011 = self.collection.selectByUnionDate("2011")
		
		self.processRecsDcsData (allRecs)
		# self.processRecsPubsId (allRecs)
		if self.dowrites:
			self.collection.write()
			print 'wrote ', self.col
		
	def processRecsDcsData (self, rec_infos):
		for rec in rec_infos:
			# print 'about to get *%s*' % rec.recId
			try:
				dcsData = getDiskDcsDataRecord (rec.recId)
			except IOError:
				print sys.exc_info()[2]
				continue
				
			rec.set('status', dcsData.getStatus())

			print rec.recId


		
	def processRecsPubsId (self, rec_infos):
		for rec in rec_infos:
			# print 'about to get *%s*' % rec.recId
			try:
				osmRecord = getDiskRecord (rec.recId)
			except IOError:
				print sys.exc_info()[1]
				continue
				
			pubsId = osmRecord.getPubsId()
			rec.set('pubsId', pubsId)
			print rec.recId
		
	def processRecsUsingDDS (self, rec_infos):
		for rec in rec_infos:
			# print 'about to get *%s*' % rec.recId
			response = self.getRecord (rec.recId)
			pubsId = response.payload.getPubsId()
			rec.set('pubsId', pubsId)
			print rec.recId
		
	# Use GetRecord dds to get GetRecord response for specified id
	def getRecord (self, recId):
		gr = GetRecord(recId)
		return gr.response

def doAll():
	for collection in collectionKeys:
		RecInfoExtender (collection)
		
if __name__ == '__main__':
	collection = 'not-fy10'
	RecInfoExtender (collection)


