"""
prerequisite in BSCS Merge and Reorg process:

	By now we've merged the BSCS into the CCS (although this won't be the case when
we do the production merge ....)

The goal of this package is to reorganize the protected directory into a
structure where all assets for a given collection are stored in a directory
named for the collection. As we move assets we have to update the protectedUrls
in the metadata.

Note: the rewrite process must convert 
	- bscs.dls.ucar.edu 
urls to 
	- ccs.dls.ucar.edu

"""
import sys, re, time, os


_CONFIG = None # populated by getConfiguration

class Configuration:
	
	def __init__ (self, args):
		for key in args.keys():
			setattr (self, key, args[key])
			
def getConfiguration():
	global _CONFIG
	if _CONFIG is None:
		host = os.environ['HOST']
		print 'host', host
		if host == 'acornvm':
			WORKSPACE = '/dls/devweb/ccs-test.dls.ucar.edu/Merge-Workspace/'
			# we are REORGING in place, using the single REORG as Merge and reorg
			mergeCurriculumRepo = os.path.join (WORKSPACE, 'REORG/curriculum/records')
			mergeUserContentRepo = os.path.join (WORKSPACE, 'MERGE/userContent/records_ccs_users')
			mergeProtectedDir = '/export/devweb/ccs-cataloging.dls.ucar.edu/docroot/protected'

			reorgCurriculumRepo = os.path.join (WORKSPACE, 'REORG/curriculum/records')
			reorgUserContentRepo = os.path.join (WORKSPACE, 'REORG/userContent/records_ccs_users')
			reorgProtectedDir = '/export/devweb/ccs-cataloging.dls.ucar.edu/docroot/protected-6-3'

		elif host == 'purg.local':
			WORKSPACE = '/Users/ostwald/Documents/Work/CCS/BSCS_Integration/5-18/5-30-data/'
			mergeCurriculumRepo = os.path.join (WORKSPACE, 'REORG/curriculum/records')
			mergeUserContentRepo = os.path.join (WORKSPACE, 'REORG/userContent/records_ccs_users')
			mergeProtectedDir = os.path.join (WORKSPACE, 'MERGE/protected')
			
			reorgUserContentRepo = os.path.join (WORKSPACE, 'REORG/userContent/records_ccs_users')
			reorgCurriculumRepo = os.path.join (WORKSPACE, 'REORG/curriculum/records')
			reorgProtectedDir = os.path.join (WORKSPACE, 'REORG/protected')
		else:
			raise Exception, 'getProtectedPath does not recognize host: "%s"' % host	
		
		_CONFIG = Configuration ({
				'mergeProtectedDir' : mergeProtectedDir,
				'mergeCurriculumRepo': mergeCurriculumRepo,
				'mergeUserContentRepo' : mergeUserContentRepo,
				'reorgProtectedDir' : reorgProtectedDir, # the reorganized protected dir
				'reorgUserContentRepo' : reorgUserContentRepo, # CCS user content records
				'reorgCurriculumRepo' : reorgCurriculumRepo
		})
	return _CONFIG
	
base_protected_url = "http://ccs.dls.ucar.edu/home/protected"
bscs_base_protected_url = "http://bscs.dls.ucar.edu/home/protected"
dps_base_protected_url = "http://ccs.dls.ucar.edu/dps/protected"

curriculum_view = None

## PROTECTED DIR
def getMergeProtectedDir ():
	"""
	the existing (old org) protected directory
	"""
	return getConfiguration().mergeProtectedDir

def getReorgProtectedDir():
	"""
	the new protected directory to which we are writing assets in directories
	named for the collection
	"""
	return getConfiguration().reorgProtectedDir

def getProtectedDir():
	"""
	depends on value of curriculum_view
	"""
	return (curriculum_view == 'reorg') and \
			getReorgProtectedDir() or getMergeProtectedDir()

def getAssetPath (url):
	"""
	convert given url to a file path in old_protected directory
	"""
	protectedDir = curriculum_view == 'reorg' and getReorgProtectedDir() or getMergeProtectedDir()
	
	# print '-protectedDir:', protectedDir
	# print '- url:', url
	# print '- base_protected_url:', base_protected_url	
	# print '- bscs_base_protected_url:', bscs_base_protected_url	
	if url.startswith(base_protected_url):
		return protectedDir + url.replace (base_protected_url, '')
	if url.startswith(bscs_base_protected_url):
		return protectedDir + url.replace (bscs_base_protected_url, '')
	if url.startswith(dps_base_protected_url):
		return protectedDir + url.replace (dps_base_protected_url, '')
	raise Exception, "not a protected URL: %s" % url
	
def getProtectedUrlForPath (path, useNewPd=False):
	"""
	convert the given path to the url that would reach it
	
	- currently looks in mergeProtectedDir (pre-reorg) by default
	- useNewPD forces use of reorgProtectedDir
	"""
	protectedDir = useNewPd and getReorgProtectedDir() or getProtectedDir()
	if 0:
		print ' = path:', path
		print ' = protectedDir: ' + protectedDir
		print ' = base_protected_url:', base_protected_url
	return base_protected_url + path.replace(protectedDir, '')

def isProtectedUrl (url):
	return url.startswith(base_protected_url)
	
def isCcsProtectedUrl (url):
	return url.startswith(base_protected_url)	

def isBscsProtectedUrl (url):
	return url.startswith(bscs_base_protected_url)
	
def isDpsProtectedUrl (url):
	return url.startswith(dps_base_protected_url)

def isAnyProtectedUrl (url):
	return isCcsProtectedUrl(url) or isBscsProtectedUrl(url) or isDpsProtectedUrl(url)
	
## USER_CONTENT	
def getMergeUserContentRepo ():
	return getConfiguration().mergeUserContentRepo

def getReorgUserContentRepo ():
	return getConfiguration().reorgUserContentRepo
	
## CURRICULUM
def getCurriculumRepo():
	return (curriculum_view == 'reorg') and \
			getReorgCurriculumRepo() or getMergeCurriculumRepo()

def getMergeCurriculumRepo():
	return getConfiguration().mergeCurriculumRepo
	
def getReorgCurriculumRepo():
	return getConfiguration().reorgCurriculumRepo
	
from reorg_shared import *

# query the repository for url:${url_pat}


