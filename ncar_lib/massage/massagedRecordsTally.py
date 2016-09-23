from tally import TallyRunner, CallbackMetadataProcessor
from recordIdListProcessor import ChangedRecordsProcessor, UnchangedRecordsProcessor
from reporter import rpClass, AllRecordsProcessor
import globals

class FieldsEndingInPeriod (TallyRunner):
	
	header = "Fields with a value ending in period"
	verbose = False

	def __init__ (self, runnerClass=AllRecordsProcessor, preprocess=0):

		self.runnerClass = runnerClass
		rpClass.preprocess = preprocess
		print "\n", self.header
		TallyRunner.__init__ (self)
	
	def myRecordProcessor (self, rp):
		"""
		for each record processed, tallies the following field
		"""
		for field in globals.library_dc_fields:
			values = rp.lib_dc_rec.getFieldValues (field)
			for val in values:
				if val[-1] == '.':
					self.myTally.tally (field)
					break
		# self.myTally.tally (rp.lib_dc_rec.getFieldValues (field))
			
	def run (self):
		self.runnerClass(self.myRecordProcessor)

	
if __name__ == "__main__":
	preprocess = 1
	runner = FieldsEndingInPeriod (AllRecordsProcessor, preprocess)
	runner.myTally



