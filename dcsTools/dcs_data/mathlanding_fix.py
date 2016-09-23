"""
Remove status entries with bogus (i.e, "1969" dates)
"""
import os, sys, re
from JloXml import DcsDataRecord, XmlUtils
from JloXml.DcsDataRecord import StatusEntry

class MathlandingUpdater (DcsDataRecord):
	
	dowrites = 0
	
	def __init__ (self, path):
		DcsDataRecord.__init__ (self, path=path)

	def repair1 (self):
		"""
		delete entries that have dates for year 1969
		"""
		print 'repair (%d)' % len (self.entryList)
		for entry in self.entryList:
			# print '-', entry.timeStamp
			if entry.timeStamp == 0.0:
				# remove this entry
				# print '\n', entry
				self.entryList.remove(entry)
				print 'removed (now %d)' % len(self.entryList)
				
	def repair (self):
		todelete = []
		entryEls = XmlUtils.getChildElements(self.entriesElement)
		for entryEl in entryEls:
			entry = StatusEntry(entryEl.toxml())
			if entry.timeStamp == 0.0:
				todelete.append(entryEl)
				
		if len(todelete) > 0:
			for el in todelete:
				self.entriesElement.removeChild(el)
			if self.dowrites:
				self.write()
				print 'repaired', self.path
			else:
				print 'WOULD HAVE repaired', self.path

	def reportEntries (self):
		print '\n', self.getId()
		for entry in self.entryList:
			if (entry.statusNote):
				print "%s - %s\n%s" % (entry.changeDate, entry.status, entry.statusNote)
			else:
				print "%s - %s" % (entry.changeDate, entry.status)


def testRec(path):
	rec = MathlandingUpdater(path)
	# print '%d entries found' % len(rec.entryList)
	rec.repair()
	# print rec
	
	if 0:
		for entry in rec.entryList:
			# print '-', entry.timeStamp
			if entry.timeStamp == 0.0:
				# remove this entry
				# print '\n', entry
				rec.reportEntries()
			
		
	
	
def testDir(dirname):
	print '\n====================================================\n'
	for filename in os.listdir(dirname):
		path = os.path.join (dirname, filename)
		testRec(path)

if __name__ == '__main__':
	dcs_data_dir = '/Users/ostwald/tmp/math_path/math_path'
	# collection = '1290084883129'
	collection = '1278566073520'
	
	collection_dir = os.path.join (dcs_data_dir, collection)
	
	recId = 'MATH-PATH-000-000-000-078'
	
	file = os.path.join (collection_dir, recId + '.XML')

			
	# testRec(file)
	testDir(collection_dir)
