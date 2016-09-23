"""
sequence:
1 - rename BSCS stds-nat to stds-nat-bscs (prefix: STD-NAT to STD-NAT-BSCS)
	see changeStdsNatKeyAndPrefix()
2 - merge bscs collections (but not the "hsbio" collections) into CCS Curriculum
	see bscsIntoCCSCurriculumMerger()
	
NOTE: now the curriculums are merged so we will be working with the recoreds and
collection_configs in the MERGED curriculum
	
3 - Rename sys-generated collections
	see changeSystemGeneratedCollectionKeys()
4 - Assign "Done" status to all item records 
	see assignDoneStatusToAllRecords()
	
NOTE: curriculums are now merged and updated for status-aware. 
	
5 - Configure DCS to point to merged curriculum AND collection_configs.
	Load/index (from scratch) in DCS and verify that all is well 
	verify number of records/collections verify all are Done
	
"""
import os, sys, re
from UserDict import UserDict
from collection_tool import CollectionTool

class Configuration:
	
	required_attrs = [
		'bscs_curriculum_records',
		'bscs_collection_config',
		'merged_curriculum_records',
		'merged_collection_config'
	]
	
	def __init__ (self, args):
		print 'Configuration'
		
		for key in args.keys():
			setattr(self, key, args[key])
			# print '- %s: %s' % (key, args[key])
			
			
"""
CONFIGURATION - the following paths must be defined
	bscs_curriculum_records
	bscs_collection_config
	merged_curriculum_records
	merged_collection_config
"""

host = os.environ['HOST']

if host == 'acornvm':
	MERGE_WORKSPACE = '/users/Home/ostwald/devel/ccs/5-18'
	bscs_curriculum_records = os.path.join (MERGE_WORKSPACE, '5-18-BSCS/records')
	bscs_collection_config = os.path.join (MERGE_WORKSPACE, '5-18-BSCS/dcs_conf/collections')
	merged_curriculum_records = os.path.join (MERGE_WORKSPACE, 'merged_curriculum/records')
	merged_collection_config = os.path.join (MERGE_WORKSPACE, 'merged_curriculum/dcs_conf/collections')

elif host == 'purg.local':
	MERGE_WORKSPACE = '/Users/ostwald/Documents/Work/CCS/BSCS_Integration/5-18/5-30-data/'
	bscs_curriculum_records = os.path.join (MERGE_WORKSPACE, 'BSCS/curriculum/records')
	bscs_collection_config = os.path.join (MERGE_WORKSPACE, 'BSCS/curriculum/dcs_conf/collections')	
	merged_curriculum_records = os.path.join (MERGE_WORKSPACE, 'MERGE/curriculum/records')
	merged_collection_config = os.path.join (MERGE_WORKSPACE, 'MERGE/curriculum/dcs_conf/collections')
	
# ensure required paths are defined
CONFIG = Configuration ({
			'bscs_curriculum_records' : bscs_curriculum_records,
			'bscs_collection_config' : bscs_collection_config,
			'merged_curriculum_records' : merged_curriculum_records,
			'merged_collection_config' : merged_collection_config
		})
	
dowrites = 1

def changeStdsNatKeyAndPrefix():
	"""
	change the prefix for the former stds-nat collection in bscs curriculum repo
	
	TODO: implment update collectionKey - currently this must be done
	manually
	"""
	key = 'stds-nat'
	prefix = 'STD-NAT'
	xmlFormat = 'comm_anno'
	new_key = 'stds-nat-bscs'
	new_prefix = 'STD-NAT-BSCS'
	new_name = 'BSCS Standards - National'

	tool = CollectionTool (CONFIG.bscs_curriculum_records, xmlFormat, key)
	tool.dowrites = dowrites
	tool.changePrefix (prefix, new_prefix)
	tool.updateCollectionDirName (new_key)
	tool.updateCollectionRecord (new_key, new_name)
	tool.updateCollectionConfig (CONFIG.bscs_collection_config, new_key=new_key, new_prefix=new_prefix)
	print "changeStdsNatKeyAndPrefix - COMPLETED"
		
def bscsIntoCCSCurriculumMerger():
	import curriculum_merger
	
	print "\nbscsIntoCCSCurriculumMerger starting ..."
	curriculum_merger.dowrites = dowrites
		
	src = CONFIG.bscs_curriculum_records
	dst = CONFIG.merged_curriculum_records
		
	merger = curriculum_merger.CurriculumRepoMerger (src, dst, dcs_data=1)
	merger.merge() 
	
"""
systemGeneratedKeysMap was constructed from the collection settings page of DCS

(e.g., '1306538472133') to the human-readable versions in systemGeneratedKeysMap

systemGeneratedKeysMap is used in changeSystemGeneratedCollectionKeys() (this module) and
also in protected.saved_resource_url_rewriting_records.py()
"""	
systemGeneratedKeysMap = {

	
	'1306538472133' : { 
		'key' : 'activities_bscs',
		'xmlFormat' : 'adn'
	},
	'1206789974136' : { 
		'key' : 'activities_iat',
		'xmlFormat' : 'adn'
	},
	'1214955173948' : { 
		'key' : 'curr_iat',
		'xmlFormat' : 'concepts'
	},
	'1206789974613' : { 
		'key' : 'tips_iat',
		'xmlFormat' : 'dlese_anno'
	},
	'1214955174534' : { 
		'key' : 'units_iat',
		'xmlFormat' : 'concepts'
	}
}

		
def changeSystemGeneratedCollectionKeys():
	"""
	The work is done in
	- merged_curriculum_records
	- merged_collection_config - e.g., .../dcs_conf/collections)

	
	This function will peform all steps involved in changing collection keys for these
	collections that currently have system-generated collection keys
	
	For each of these collections, changing the collection key involves:
	- updateCollectionRecord (new_key)
	- updateCollectionDirName (new_key);
	- updateCollectionConfig (collection_config_dir, new_key=new_key, new_prefix="FOOBERRY");
	
	"""
	
	
	# repo_base and collections_config dirs are in MERGED curriculum
	
	for old_key in systemGeneratedKeysMap.keys():
		info = systemGeneratedKeysMap[old_key]
		xmlFormat = info['xmlFormat']
		new_key = info['key']
		tool = CollectionTool (CONFIG.merged_curriculum_records, xmlFormat, old_key)
		tool.dowrites = dowrites
		tool.updateCollectionRecord (new_key)
		tool.updateCollectionDirName (new_key)
		tool.updateCollectionConfig (CONFIG.merged_collection_config, new_key=new_key)
		print 'FINSHED changing key to "%s"\n' % new_key

def assignDoneStatusToAllRecords():
	import assign_statuses
	assign_statuses.dowrites = dowrites
	# if  host == 'acornvm':
		 # merged_dcs_data_dir = os.path.join (MERGE_WORKSPACE, 'merged_curriculum/records/dcs_data')
	# else:
		# raise Exception, "unrecognized host: %s" % host
	merged_dcs_data_dir = os.path.join (CONFIG.merged_curriculum_records, 'dcs_data')
	assign_statuses.walkRepo(merged_dcs_data_dir)

if __name__ == '__main__':
	# changeStdsNatKeyAndPrefix()
	
	# bscsIntoCCSCurriculumMerger() 
	
	# changeSystemGeneratedCollectionKeys()
	
	assignDoneStatusToAllRecords()
	
