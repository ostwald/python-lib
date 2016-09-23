"""
update metadata based on vocab terms which are being changed.

input spreadsheets for various vocab fields (instName, pubName, eventName). 
  each spreadsheet has two columns:
    Bad Term | Good Term

affect: all osm records in the repository containing given Bad Term must be 
modified to replace it for Good Term
"""
import os, sys
# from JloXml import XmlUtils
# from ncar_lib.osm import osmRecord
# from ncar_lib.repository import RepositorySearcher, OsmSearchResult
# from ncar_lib.vocabs.termSearch import TermSearcher
# from ncar_lib.repository.reports.vocabs import vocab_data
# from ncar_lib.repository import CachingRecordManager, CachedRecordError

from osm_updater import getRecordManager, replaceVocabTerm

	
TEST_RECORD = 'OSGC-000-000-002-098'
	
def pubNameTester(osmRec=None):
	badTerm = 'Journal of Geophysical Research - Atmospheres'
	goodTerm = 'Journal of Geophysical Research-Atmospheres'
	indexField = 'pubName'
	if osmRec is None:
		recMgr = getRecordManager()
		osmRec = recMgr.getRemoteRecord(TEST_RECORD)
	replaceVocabTerm (badTerm, goodTerm, indexField, osmRec)
	return osmRec
	
def eventNameTester(osmRec=None):
	badTerm = '80st AMS Annual Meeting'
	goodTerm = '80th AMS Annual Meeting'
	indexField = 'eventName'
	if osmRec is None:
		recMgr = getRecordManager()
		osmRec = recMgr.getRemoteRecord(TEST_RECORD)
	replaceVocabTerm (badTerm, goodTerm, indexField, osmRec)
	return osmRec
	
def instNameTester(osmRec=None):
	badTerm = 'University Corporation for Atmospheric Research (UCAR)'
	goodTerm = 'University Corporation for Atmospheric Research'
	indexField = 'instName'
	if osmRec is None:
		recMgr = getRecordManager()
		osmRec = recMgr.getRemoteRecord(TEST_RECORD)
	replaceVocabTerm (badTerm, goodTerm, indexField, osmRec)
	return osmRec
	
if __name__ == '__main__':
	recMgr = getRecordManager()
	osmRec = recMgr.getRemoteRecord(TEST_RECORD)
	# pubNameTester(osmRec)
	instNameTester(osmRec)
	# eventNameTester(osmRec)
	print osmRec
