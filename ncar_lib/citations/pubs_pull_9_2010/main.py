"""
Mission:
Get all PUBs records EXCEPT -
    * FY 2010 records
    * Citations - PUBS Refereed (2838)

FY2010 Records are in H:/python-lib/ncar_lib/citations/pubs/PUBS_FY2010_metadata
	these records are in Citation format
    the pub_id is at /record/pub_id

	see fy2010ids.getFY2010Ids
	
PUBS Refereed citations
	see pubs_refereed.getPubsRefdIds
	
get ALL pubs:
	Use PubsProcessor
	
NOTES:
	- author info comes from "author" table (not-optimized)
	- editors passed through as is (from "publication record")
	
"""
import os, sys
from fy2010ids import getFY2010Ids
from pubs_refereed import getPubsRefdIds
from ncar_lib.citations import Citation
from ncar_lib.citations.pubs import PubsProcessor

fy2010Ids = getFY2010Ids()
# pubsRefdIds = getPubsRefdIds()

class PubsNotFY2010 (PubsProcessor):
	destDir = "PUBS-NOT-FY2010"
	id_prefix = "PUBS-NOT-FY2010"
	select_query = "" # grab everything
	# select_query = "pub_id = 201219" # grab JUST 201219, which has bad chars ...
	optimizeAuthorData = 0 # use author data from the author table (initials only)
	
	def __init__ (self, startid=None, limit=None, write=1):
		self.citations = []
		
		# IMPORTANT - cast ids to int (cause that's what pub_id's are)
		self.stop_ids = map (int, fy2010Ids)
		print "%d stop_ids" % len (self.stop_ids)

		PubsProcessor.__init__ (self, startid=startid, limit=limit, write=write)
	
	def processRecords (self):
		"""
		process all by FY2010 records
		"""
		for rec in self.records:
			data = self.makeDataDict (rec)
			pub_id = rec['pub_id']
			
			if pub_id in self.stop_ids:
				# print "skipping", pub_id
				pass
			else:
				citation = Citation (data, self.makeId(self.idcounter))
				self.citations.append (citation)
				if self.write:
					citation.write (os.path.join (self.destDir, citation.id+'.xml'))
				else:
					# print citation
					if self.reccounter % 200 == 0:
						print "%d/%d" % (self.reccounter, len(self.records))
					
				self.idcounter = self.idcounter + 1
			self.reccounter = self.reccounter + 1
			if self.reccounter >= self.limit: break
	
if __name__ == '__main__':
	puller = PubsNotFY2010 (limit=None, write=1)
	print "%d records pulled from db" % len(puller.records)
	citations = puller.citations
	print "%d citation records" % len(citations)
	# print citations[0].encode('utf-8')

