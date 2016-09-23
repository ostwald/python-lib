"""
Collection config and Collection Record Mover

We are migrating all DLESE collections ("adn" and "dlese_anno") to NSDL.

The metadata and dcs_data records can be moved by hand.

This file contains tools to migrate the other collection components:
- collection config file
- collection record

NOTE: this module has nothing to do with the CollectionOfCollections

"""
import sys, os, time, shutil
from masterCollection import MasterCollection
from bscs.collection_tool import CollectionTool
from JloXml import DleseCollectRecord, XmlUtils

dowrites = 0

dlese_base = '/Users/ostwald/Desktop/DLESE_MIGRATION/DLESE' #DLESE
nsdl_base = '/Users/ostwald/Desktop/DLESE_MIGRATION/NSDL' # NSDL

dlese_records = os.path.join (dlese_base, 'records') #DLESE
nsdl_records = os.path.join (nsdl_base, 'records') #NSDL

dlese_collection_configs = os.path.join(dlese_base, 'dcs_conf/collections')
nsdl_collection_configs = os.path.join(nsdl_base, 'dcs_conf/collections')

def get_nsdl_collection_keys():
	nsdl_collection_records = get_nsdl_collection_records()
	return nsdl_collection_records.getValues('key')
	
def get_nsdl_collection_records():
	"""
	returns MasterCollection instance containing NSDL collection records
	"""
	nsdl_collect_dir = os.path.join (nsdl_records, 'dlese_collect', 'collect')
	return MasterCollection(nsdl_collect_dir, DleseCollectRecord)	

def findDleseCollectionRecord(field, value):
	"""
	returns first DleseCollectRecord having the specified value for specified field
	"""
	dlese_collect_dir = os.path.join (dlese_records, 'dlese_collect', 'collect')
	for filename in filter (lambda x:x.endswith('xml'), os.listdir(dlese_collect_dir)):
		path = os.path.join (dlese_collect_dir, filename)
		rec = DleseCollectRecord (path=path)
		if (rec.get(field) == value):
			return rec
			

nsdl_keys = get_nsdl_collection_keys()
			
def copyDleseCollectionRecord(key):
	"""
	copies DLESE collection record for specified key
	into NSDL collection records
	"""
	record = findDleseCollectionRecord ('key', key)
	if not record:
		raise KeyError, 'deleseCollectionRecord not found for %s' % key
	#now we want to rename the record
	record.setId(key)
	
	# create the dest path in nsdl collections
	nsdl_collect_dir = os.path.join (nsdl_records, 'dlese_collect', 'collect')
	dest = os.path.join (nsdl_collect_dir, key+'.xml')
	
	# check to see if file exists
	if os.path.exists(dest):
		raise KeyError, "nsdl collection record already exists for %s" % key
		
	# check to see if collection key exists!!
	if key in nsdl_keys:
		raise KeyError, "nsdl key already exists for %s" % key
		
	if dowrites:
		record.write (path=dest)
		print "wrote to", dest
	else:
		print 'Would have written record to %s' % dest
		# print record
	

# for EACH collection

# find the collection record
# copy it into nsdl repo

# find collection config
# copy it into nsdl collection config
def findCollectionConfig (key):
	"""
	finds DLESE collection config for given key
	"""
	filename = key+'.xml'
	path = os.path.join (dlese_collection_configs, filename)
	if not os.path.exists(path):
		raise KeyError, "dlese collection config not found for %s" % path
	return path
	
def moveCollectionConfig(key):
	"""
	copies DLESE collection config for given key into NSDL collection configs
	"""
	filename = key+'.xml'
	collection_config = findCollectionConfig (key)
	newpath = os.path.join (nsdl_collection_configs, filename)
	if os.path.exists(newpath):
		raise KeyError, 'nsdl collection config already exists for %s' % key
		
	if dowrites:
		return shutil.copyfile (collection_config, newpath)
	else:
		print 'Would have copied %s to %s' % (filename, newpath)
	

# copy collection dir into dest rep
# copy collection dcs_data dir into dest rep

def testGet_nsdl_collection_keys():
	for key in get_nsdl_collection_keys():
		print '-', key
	
def testFindCollectionRecord():
	foo = findDleseCollectionRecord('key', 'dcc')
	if foo:
		print foo
	else:
		print 'not found'
		
def main():
	"""
	for each collection key for adn and dlese_anno xmlFormats,
	- copy the DLESE collection record to NSDL
	- copy the DLESE collection config file to NSDL
	"""
	for xmlFormat in ['adn', 'dlese_anno']:
		print '\n', xmlFormat
		dlese_format_dir = os.path.join (dlese_records, xmlFormat)
		for key in os.listdir(dlese_format_dir):
			print '-', key
			copyDleseCollectionRecord(key)
			moveCollectionConfig(key)

if __name__ == '__main__':
	# moveCollectionConfig ("dcc")
	# copyDleseCollectionRecord("dcc")
	# testGet_nsdl_collection_keys()
	main()
