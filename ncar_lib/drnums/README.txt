Start out with a list of asset file names for selected collections, derived from nldr.
collections: asr.txt  manuscripts.txt  monographs.txt  technotes.txt  theses.txt

Compute A list of DR numbers for which no asset was found - method: using
asset_map.findUnmatchedDRNumbers, which compares the original list of DR numbers
from scrape (input/originalDRMappings.txt) with a list of asset file names currently
in the repository (/web/nldr)

--------------------------------------------------------------------------------

There were several DR numbers for which an asset wasn't found. It turns out
these assets had been renamed when the metadata record was moved from it's
original collection. The original/annotated list is in output/DR_Num_Notes.txt.
This file was compressed into input/NDR_Num_Hand_mappings.py so it could be read
by line_data_reader.py.

These DR Numbers were mapped to RecordID by hand - see input/DR_Num_Hand_mappings.txt

--------------------------------------------------------------------------------

Using original mappings plus the hand-mappings, we create an output xml file that maps
DR numbers to RecordIDs. This is done (see dr_2_record_ids.DR2RecIdMappingsby):
  For each DR number, 
  	use assetID
		search NLDR for the record that contains assetID - keep ID
		
output: output/dr_2_recId_mappings.xml

--------------------------------------------------------------------------------

To analyze the gaps in DR numbers, we used dr_mappings_verifier.py, which counts
contiguous DR numbers and lists those that are not yet mapped to recordIDs. The
output of dr_mappings_verifier.py were originally saved in
output/missing_dr_analysis_incomplete.txt and later completed as
input/gap_dr_analysis.txt, which is used as input to refine the data used by
"DR2RecIdMappings" & "makeURLResolverMappings.pyURLResolverMappings".

--------------------------------------------------------------------------------

FINALLY - to make the final version of accessionNumberMappings.xml, we need to incorporate the
data from gap_dr_analysis.txt into the input to URLResolverMappings ...

see gapPlugger.py

to verify, see dr_mappings_verifier.py - the output of this should be the same as the DR#s in 
gapPlugger.GapAnalysisMappings.unMapped

and they are as of 10/29/10
