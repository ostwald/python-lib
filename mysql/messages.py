"""
SELECT `collKey`, `id`, `recCheckDate`, `msgType`, `url`
FROM `idmapMessages`
WHERE `collKey`='tbox' and `msg` is not NULL


# grab the messages (warnings) sent for a particular collection
# note: recCheckDate must be specified ... but we could also just grab all
# sorted and drop the ones that aren't most recent ...

SELECT `collKey` , `id` , `recCheckDate` , `msgType` , `url`
FROM `idmapMessages` 
WHERE `collKey` ='tbox' and `recCheckDate` = '2008-01-23 23:00:03'
ORDER BY `idmapMessages`.`recCheckDate`  DESC

"""
import string
import time
from UserDict import UserDict
from UserList import UserList
from IdmapDB import WebPubDB, WebTestDB, BolideDB
from collectionsTable import Collections

class Messages (UserList):

	"""
	wrapper for an idmapMessages table
	this is a huge (2+ million recs) table, so we work with only a collection at
	a time

	simply maintains a list of messages, with the fields of the schema. the list
	is ordered by record id
	
	"""

	schema = ["collKey", "id", "recCheckDate", "msgType", "url"]

	def __init__ (self, db, collKey):
		self.db = db
		self.collKey = collKey
		rows = db.doSelect (self.makeQueryString())
		print (self.makeQueryString())
		UserList.__init__ (self)
		print len(rows), " found"

		refdate = None
		for row in rows:
			rec = {}
			for index in range(len(self.schema)):
				rec[self.schema[index]] = row[index]

			if refdate is None:
				refdate = rec['recCheckDate']
			elif rec['recCheckDate'] != refdate:
				break

			self.append (rec)			

	def getCollCheckDate (self):
		c = Collections (self.db)
		return c.getCollCheckDate (self.collKey)

	
	def makeQueryString (self):
		"""
		finds messages generated the last time this collection was checked
		"""
		schemaStr = string.join (self.schema, ', ')
		checkDate = self.getCollCheckDate()
		return """SELECT %s
	           FROM idmapMessages
			   WHERE collKey = '%s' and recCheckDate = '%s'
			   ORDER BY idmapMessages.id""" % \
	           (schemaStr, self.collKey, checkDate )

def tester1 ():
	"""

	"""
	db = BolideDB()
	collKey = "dcc"
	msgs = Messages (db, collKey)
	print "%d messages for this date" % len(msgs)
	for row in msgs:
		print row['id'], row['recCheckDate'], row['msgType'], row['url']

	print msgs.getCollCheckDate()	
			   
if __name__ == "__main__":
	tester1()
