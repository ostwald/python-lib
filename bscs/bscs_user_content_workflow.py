"""
bscs_user_content_workflow.py
"""
import sys, os
from user_content_merger import CollectionMerger, UserCollectionMerger, UserContentMerger
import bscs

dowrites = 1

# Configuration
host = os.environ['HOST']

class Configuration:
	
	def __init__ (self, args):
		for key in args.keys():
			setattr (self, key, args[key])
			
def getConfiguration():

	if host == 'purg.local':
		WORKSPACE = '/Users/ostwald/Documents/Work/CCS/BSCS_Integration/5-18/5-30-data'
		bscs_user_content_repo = os.path.join (WORKSPACE, 'BSCS/userContent/records_ccs_users/')
		merged_user_content_repo = os.path.join (WORKSPACE, 'MERGE/userContent/records_ccs_users/')
	elif host == '??':
		bscs_user_content_repo = '/Users/ostwald/devel/dcs-repos/merge-workspace/ccs-bscs/ccs_user_content/records_ccs_users'
		merged_user_content_repo = '/Users/ostwald/devel/dcs-repos/merge-workspace/ccs-merged/records_ccs_users'
	else:
		raise Exception, 'Unrecognized host: ' + host
		
	return Configuration ({
			'bscs_user_content_repo' : bscs_user_content_repo,
			'merged_user_content_repo' : merged_user_content_repo
	})

def mergeUserContent():
	
	host = os.environ['HOST']
	CONFIG = getConfiguration()
	src_repo = CONFIG.bscs_user_content_repo # where the new records come from
	dst_repo = CONFIG.merged_user_content_repo # where the new records (from bscs) go

	toIgnore = map (lambda x:x.id , bscs.bscs_ccs_dup_users)
	test_mode = not dowrites
	merger = UserContentMerger (src_repo, dst_repo, toIgnore, test_mode)
	merger.merge()
	if not test_mode:
		print "User Content has been merged"

def testMergeUserContent():
	
	CONFIG = getConfiguration()
	src_repo = CONFIG.bscs_user_content_repo # where the new records come from
	dst_repo = CONFIG.merged_user_content_repo # where the new records (from bscs) go

	toIgnore = map (lambda x:x.id , bscs.bscs_ccs_dup_users)	
	test_mode = not dowrites
	if 0:
		rel_path = 'dlese_anno/ccsprivateannos'
		src_col = os.path.join (src_repo, rel_path)
		dst_col = os.path.join (dst_repo, rel_path)
		merger = CollectionMerger (src_col, dst_col, test_mode)
		merger.merge()
	elif 1:
		rel_path = 'userdata/ccsusers'
		src_col = os.path.join (src_repo, rel_path)
		dst_col = os.path.join (dst_repo, rel_path)
		merger = UserCollectionMerger (src_col, dst_col, toIgnore, test_mode)
		merger.merge()

if __name__ == '__main__':
	# testMergeUserContent()
	
	mergeUserContent()

