"""
helper
"""
import os, sys
from masterCollection import MasterCollection
from JloXml import DleseCollectRecord, XmlUtils

# collectionKeyPlucker



if __name__ == '__main__':
	dlese_collect_master_dir = '/Users/ostwald/Desktop/DLESE_MIGRATION/DLESE/records/dlese_collect/dcr'
	master = MasterCollection(dlese_collect_master_dir, DleseCollectRecord)
	
	contrib_dict = {}
	for rec in master:
		
		contribs = rec.getContributorsForContacts()
		for contrib in contribs:
			contrib_dict[contrib.getFullName()] = contrib
			
	for contrib in contrib_dict.values():
		print '-', contrib
