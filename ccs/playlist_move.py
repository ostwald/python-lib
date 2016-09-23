import os, sys, re
from repo import Repo

host = os.environ['HOST']
if host == 'purg.local':
	src_repo_base = '/Users/ostwald/devel/dcs-repos/dds-ccs-dev/ccs_user_content/records_ccs_users/'
elif host == 'dls-rs1':
	src_repo_base = '/dls/www/ccs.dls.ucar.edu/ccs_user_content/records_ccs_users'
	
"""
for each resourceId in a list, 
	find the annos (user saves) for that resource
	check if there is an anno by the current User
	 - (DUH) there should be, since these resources are on the user's playlist!!
"""
	
def findUserAnnos (repo, resIds, userId):
	"""
	resIds are the resources in a playlist.
	here we find the user's saves for these resources.
	"""
	annoPaths=[];add=annoPaths.append
	for resId in resIds:
		try:
			path = repo.findAnnoPath(resId, userId)
			add (path)
		except Exception, msg:
			print 'Error: ', msg
	return annoPaths
			
	
	
if __name__ == '__main__':
	host = os.environ['HOST']

	if host == 'dls-rs1':
		userId = 'DPS-1247001681454' # margaret
		resourceId = '1374202578944'
		repo_base = '/dls/www/ccs.dls.ucar.edu/ccs_user_content/records_ccs_users'
	if host == 'purg.local':
		userId = '1247065132457'
		resourceId = '1268089830379'
		repo_base = '/Users/ostwald/devel/dcs-repos/dds-ccs-dev/ccs_user_content/records_ccs_users/'
		resIds = [
			'1271000343182',
			'1254607776664',
			'1248387485269'
			]
			
	repo = Repo(repo_base)
	# print findAnnoPath (resourceId, userId)
	findUserAnnos(repo, resIds, userId)
						 
	# parseAnnoId('CCS-ANNO-RESOURCE-DPS-1247001681465-1262103110670')
