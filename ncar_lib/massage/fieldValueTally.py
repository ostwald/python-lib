from tally import TallyRunner, CallbackMetadataProcessor
from recordIdListProcessor import ChangedRecordsProcessor, UnchangedRecordsProcessor
import globals

class UniqueFieldValues (TallyRunner):
	
	header = "??"
	verbose = False

	def __init__ (self, field, recAttr, runnerClass=CallbackMetadataProcessor):
		self.header = field
		self.field = field
		self.recAttr = recAttr
		self.runnerClass = runnerClass
		print "\nUnique '%s' values in '%s' records using '%s'" % (field, recAttr, runnerClass.__name__)
		TallyRunner.__init__ (self)
	
	def myRecordProcessor (self, rp):
		"""
		for each record processed, tallies the following field
		"""
		
		rec = getattr (rp, self.recAttr)
		
		self.myTally.tally (rec.getFieldValues (field))
		# self.myTally.tally (rp.lib_dc_rec.getFieldValues (field))
			
	def run (self):
		self.runnerClass(self.myRecordProcessor)

		
def tallyWorkingRecords (field):
	runner = UniqueFieldValues (field, 'lib_dc_rec', CallbackMetadataProcessor)
	return runner.myTally
	
def tallyUnchangedRecords (field):
	runner = UniqueFieldValues (field, 'ncar_rec', UnchangedRecordsProcessor)
	return runner.myTally
	
def tallyChangedRecords (field):
	runner = UniqueFieldValues (field, 'ncar_rec', ChangedRecordsProcessor)
	return runner.myTally
	
def tallyNCARRecords (field):
	runner = UniqueFieldValues (field, 'ncar_rec', CallbackMetadataProcessor)
	return runner.myTally
	
def tallyFieldsEndingInPeriod(notUsedAttr="None"):
	runner = FieldsEndingInPeriod (CallbackMetadataProcessor)
	return runner.myTally
	
if __name__ == "__main__":
	field = "dc:rights"
	if not field in globals.library_dc_fields:
		msg = "Bogus field: '%s'" % field
		raise Exception, msg
	# tallyUnchangedRecords
	# tallyChangedRecords
	# tallyWorkingRecords
	# tallyNCARRecords
	tallyFunction = tallyWorkingRecords
	tally = tallyFunction (field)



