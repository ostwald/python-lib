import os, sys, re

class Repo:

	def __init__ (self, repo_base):
		self.repo_base = repo_base
		self.playlist_dir = os.path.join (repo_base, 'playlist/ccsplaylists')
		self.resource_dir = os.path.join (repo_base, 'adn/ccsusersubmittedresources')
		self.anno_dir = os.path.join (repo_base, 'dlese_anno/ccsprivateannos')
	
	def verifyPath (self, path):
		if not os.path.exists(path):
			raise Exception, 'ERROR: file not found at %s' % path
		return path
	
	def findResourcePath (self, id):
		path = os.path.join (self.resource_dir, id+'.xml')
		return self.verifyPath(path)
	
	def findAnnos (self, resourceId):
		"""
		return ids of annos for this resource
		"""
	
		def filterFn (filename):
			id, ext = os.path.splitext (filename)
			if ext != '.xml':
				return False
	
			try:
				resId, userId = self.parseAnnoId (id)
				return resId == resourceId
			except Exception, msg:
				print 'ERROR filterFn: %s' % msg
			return False
	
		filenames = filter( filterFn, os.listdir (self.anno_dir))
		print 'found %d files' % len(filenames)
		for name in filenames:
			print '- ', name
		
	
	def makeAnnoId(self, resId, userId):
		"""
		CCS-ANNO-RESOURCE-DPS-1247001681465-1262103110670.xml
		"""
	
		return 'CCS-ANNO-RESOURCE-%s-%s' % (userId, resId)
	
	def findAnnoPath (self, resId, userId):
		annoId = self.makeAnnoId (resId, userId)
		path = os.path.join (self.anno_dir, annoId+'.xml')
		return self.verifyPath(path)
	
	def parseAnnoId (self, annoId):
		"""
		- returns tuple: resourceId, userId
		- raises exception if provided annoId cannot be parsed
		"""
		pat = re.compile('CCS-ANNO-RESOURCE-(.*)-([\d]*)')
		
		m = pat.match(annoId)
		if m:
			
			# resourceId, userId
			return m.group(2), m.group(1)
		raise Exception, "Parse error: could not parse '%s'" % annoId

	def parseTester (self):
		userId = 'DPS-1247001681454' # margaret
		resourceId = '1374202578944'
		annoId = self.makeAnnoId (userId, resourceId)
		print 'annoId:', annoId
		newResId, newUserId = self.parseAnnoId(annoId)
		print 'newResId: %s newUserId: %s' % (newResId, newUserId)

# purg ID

if __name__ == '__main__':
	host = os.environ['HOST']

	if host == 'dls-rs1':
		userId = 'DPS-1247001681454' # margaret
		resourceId = '1374202578944'
		repo_base = '/dls/www/ccs.dls.ucar.edu/ccs_user_content/records_ccs_users'
	if host == 'purg.local':
		userId = 'DPS-1247001681462'
		resourceId = '1268089830379'
		repo_base = '/Users/ostwald/devel/dcs-repos/dds-ccs-dev/ccs_user_content/records_ccs_users/'
		
	repo = Repo(repo_base)
	# print findAnnoPath (resourceId, userId)
	repo.findAnnos(resourceId)
						 
	# parseAnnoId('CCS-ANNO-RESOURCE-DPS-1247001681465-1262103110670')
