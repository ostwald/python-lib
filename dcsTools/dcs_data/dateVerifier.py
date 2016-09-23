import os, sys, re
from walkingUpdater import WalkingUpdater, Updater
from nsdlToLdap_Globals import DcsDataRecord
import nsdlToLdap_Globals
# from JloXml.DcsDataRecord import StatusElement
# from DcsDataRecord_v1 import DcsDataRecord_v1
# DcsDataRecord = DcsDataRecord_v1
# del DcsDataRecord_v1

# datePat = re.compile ("[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}Z");
datePat = nsdlToLdap_Globals.datePat

class DateVerifier (DcsDataRecord):
	"""
	extract all dates from record:
		- lastTouchDate
		- changeDates
		- ndrSync
		
	test each for the form: 2009-08-03T15:57:16Z
	
	example call: 
		errRpt = DateVerifier (dcsDataRecord_Path_).reportErrors()
	"""
	
	
	def __init__ (self, path):
		DcsDataRecord.__init__ (self, path=path)
		
		self.lastSync = self.getLastSyncDate()
		self.lastTouch = self.getLastTouchDate()
		self.changeDates = self.getChangeDates()
		
		self.errors = self.verify()
		
	def reportStr (self):
		print '\n' + self.getId()
		print "\tlastTouch: %s" % self.lastTouch
		print "\tlastSync: %s" % self.lastSync
		if self.changeDates:
			print "\tentryDates"
			for date in self.changeDates:
				print "\t  %s" % date
		
	def reportErrors (self, verbose=1):
		if self.errors:
			print '\n' + self.getId()
			print "\tlastTouch: %s" % self.lastTouch
			print "\tlastSync: %s" % self.lastSync
			if self.changeDates:
				print "\tentryDates"
				for date in self.changeDates:
					print "\t  %s" % date
		elif verbose:
			print '\n%s - no errors' % self.getId()

				
	def getChangeDates (self):
		return map (lambda x: x.changeDate, self.entryList)

	def verify (self):
		s=[];add=s.append
		try:
			self.verifyDate (self.lastTouch, 'lastTouch')
		except:
			add (sys.exc_info()[1])
		try:
			self.verifyDate (self.lastSync, 'lastSync')
		except:
			add (sys.exc_info()[1])
		if self.changeDates:
			for cd in self.changeDates:
				try:
					self.verifyDate (cd, 'changeDate')
				except:
					add (sys.exc_info()[1])
		return s
		
	def verifyDate (self, datestr, label):
		if datestr is not None and not datePat.match (datestr):
			raise ValueError, "%s: %s" % (label, datestr)
	
class DateVerifyingUpdater (Updater):
	
	verbose = 0
	
	def __init__ (self, path):
		self.rec = DateVerifier (path)
		self.rec.reportErrors(self.verbose)
			
class WalkingEditorUpdater (WalkingUpdater):
	"""
	recursively visits an entire directory structure and update all the .xml
	files it finds
	"""
	verbose = 0
	UPDATER_CLASS = DateVerifyingUpdater
		
def verifyTester (dcs_data_dir):
	path = os.path.join (dcs_data_dir, "res_qual/1251315332242/TAAAS-000-000-000-007.xml")
	rec = DateVerifier(path=path)
	rec.reportStr()
	print "reportErrors:"
	rec.reportErrors()
	if (rec.errors):
		print "errors"
		for e in rec.errors:
			print '\t%s' % e
			
if __name__ == '__main__':
	# dcs_data_dir = "H:/Documents/NSDL/TransitionToLdap/Data_Manipulation/dcs_data"
	# dcs_data_dir = "/home/ostwald/Documents/NSDL/TransitionToLdap/Data_Manipulation/dcs_data"
	dcs_data_dir = nsdlToLdap_Globals.DCS_DATA_DIR
	baseDir = os.path.join (dcs_data_dir, "msp2")
	WalkingEditorUpdater(dcs_data_dir)
