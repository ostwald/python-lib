"""
classes to re-run the SAT_Eval task for only the state of Massachusetts.

	# step 1 - create suggestionSets
		createMassSuggestionSets()
	# step 2 - write spreadsheets from suggestionsets
		writeSpreadSheets()
"""

import os, sys
from SampleSetManager import SuggestionSet
from SpreadSheetBuilder import SpreadSheetBuilder
from asn import makeFullId, getNumId

if sys.platform == 'win32':
	python_lib_dir = "H:/python-lib"
else:
	python_lib_dir = "/home/ostwald/python-lib"
	
sat_eval_dir = os.path.join (python_lib_dir, "SAT_Eval")

class MassSuggestionSets:

	# out_dir has to ALREADY EXIST ..
	out_dir = os.path.join (sat_eval_dir, "massachusetts_data", "suggestionSets")
	
	def __init__ (self):

		suggestionSet_dir = os.path.join (sat_eval_dir, "suggestionSets")
		
		for filename in os.listdir (suggestionSet_dir):
			root, ext = os.path.splitext (filename)
			group, band, idNum = root.split ('_')
			suggestionSet = SuggestionSet (makeFullId (idNum), group, band)
			suggestionSet.setStateList (["Massachusetts"])
			suggestionSet.load()
			# suggestionSet.report()
			suggestionSet.writeXML (os.path.join (self.out_dir, suggestionSet.filename))
			print ("wrote %s" % suggestionSet.filename)
			
class MassSpreadSheetBuilder (SpreadSheetBuilder):
	asnDocDir = os.path.join (python_lib_dir, "asn/standards-documents/localized/")
	
	# out_dir has to ALREADY EXIST ..
	outDir = os.path.join (sat_eval_dir, "massachusetts_data", "spreadsheets")
	nsesDoc = "1995-NSES-v1.3.0-Science-082007.xml"
			
def createMassSuggestionSets():
	"""
	create suggestionsets for Massachusetts and write them to disk
	in the "suggestionSets" directory
	"""
	MassSuggestionSets()
	
def spreadSheetBuilderTester():
	data_dir = "massachusetts_data/suggestionSets"
	filename = "Subject_5-8_S100A83D.xml"
	builder =  MassSpreadSheetBuilder (data_dir)
	print builder.outDir
	builder.writeSheet (filename)
	
def writeSpreadSheets ():
	data_dir = "massachusetts_data/suggestionSets"
	builder =  MassSpreadSheetBuilder (data_dir)
	builder.writeAll ()
	
if __name__ == '__main__':
	# step 1 - create suggestionSets
	#createMassSuggestionSets()
	# step 2 - write spreadsheets from suggestionsets
	writeSpreadSheets()
