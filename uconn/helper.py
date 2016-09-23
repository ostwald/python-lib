"""
helper.py

use Plucker to get collection keys from dlese_collect and (oai) setSpecs from ncs_collect

"""
import os, sys, time
from plucker import Plucker
from nsdl import NCSCollectRecord
from JloXml import DleseCollectRecord, XmlUtils


def get_ncs_collect_setSpecs():
	
	# setSpecPlucker
	ncs_collect_master = '/Users/ostwald/Desktop/DLESE_MIGRATION/NSDL/records/ncs_collect/1201216476279/'
	# field = 'collSetSpec'
	field = 'oaiSetSpec'
	return Plucker(field, ncs_collect_master, NCSCollectRecord).getValues()

def get_dlese_collection_keys():
	# collectionKeyPlucker
	dlese_collect_master = '/Users/ostwald/Desktop/DLESE_MIGRATION/DLESE/records/dlese_collect/dcr'
	field = 'key'
	return Plucker(field, dlese_collect_master, DleseCollectRecord).getValues()

def reporter():
	ncs_collect_setSpecs = get_ncs_collect_setSpecs()
	print "%d ncs_collect_setSpecs found" % len(ncs_collect_setSpecs)
	
	dlese_collect_keys = get_dlese_collection_keys()
	print "%d dlese_collect_keys found" % len(dlese_collect_keys)
	
	inNsdl = filter (lambda key:key in ncs_collect_setSpecs, dlese_collect_keys)
	print "these (%d) dlese collections are in nsdl already" % len(inNsdl)
	for key in inNsdl:
		print '-', key
			
	notInNsdl = filter (lambda key:key not in ncs_collect_setSpecs, dlese_collect_keys)
	print "these (%d) dlese collections are Not in nsdl" % len (notInNsdl)
	for key in notInNsdl:
		print '-', key


if __name__ == '__main__':
	
	reporter()
