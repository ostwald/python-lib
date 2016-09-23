"""
Updates both the metadata and assets (located in _protected_ directory

Searching for records that have protectedUrls
- RepoWalker - an engine that walks the curriculum repo
and calls "action" on each record containing protectedUrl(s).

Standalone scripts - these instantiate RepoWalker and pass in
a function to do their work (tally, reort, cache, update):

- reportFormatTally() - report number of protectedUrls found by format
- reportMissingAssets() - report urls that do not resolve to assets
- doCacheUrls() - write protectedUrls to file on disk
- doUpdate - write protectedUrls and place cataloged assets in appropriate
place in protected dir

NOTE: Run Update with dowrites = False to test

"""
import os, sys, re, shutil
from repo import RepositorySearcher
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import *
from url_rewriting_records import urlRewritingRecordClasses, URLRewritingRecord, \
				AssetNotFoundException

# CURRICULUM_REPO_BASE = '/Users/ostwald/devel/dcs-repos/reorg-workspace/dcs/records'
		
dowrites = 0
	
class RepoWalker:
	"""
	Traverse the file-based repository and invoke an action function
	on each record having one or more protectedUrl
	
	Only recognizes and acts up records whose format is represented
	in the url_rewriting_records.urlRewritingRecordClasses dict 
		- adn, assessments, dlese_anno and ncs_item
	
	"""
	verbose = 1
	skip_xmlFormats = ['dcs_data', 'trash']
	
	def __init__ (self, curriculum_repo_base, action=None):
		URLRewritingRecord.dowrites = dowrites
		self.curriculum_repo_base = curriculum_repo_base
		self.action = action or self.default_action
		self.errors = []
		
		print 'RepoWalker - repoBase:', self.curriculum_repo_base
		
		self.walkRepo()
		
	def walkRepo (self):
		"""
		skip dcs_data for now. it should be called as a repo, so we should call walkRepo
		with the dcs_data directory (EVENTUALLY)
		
		calls self.action on all records with protectedUrls
		- whether a record has a protectedUrl is determined by URLRewritingRecord
		"""
		def acceptXmlFormat(xmlFormat):
			if xmlFormat in self.skip_xmlFormats: return 0
			if not urlRewritingRecordClasses.has_key(xmlFormat): return 0
			return 1
		
		repo_base = self.curriculum_repo_base
		self.formatTally = {}
		self.errors = []
		
		for xmlFormat in filter (acceptXmlFormat, subDirNames(repo_base)):
			print '\n', xmlFormat
			xmlFormatPath = os.path.join (repo_base, xmlFormat)
			
			for collection in subDirNames (xmlFormatPath):
				# if (collection != 'comment_bscs'): continue
				collectionPath = os.path.join (xmlFormatPath, collection)
				#print ' - ', collection
				sys.stdout.write('.')
				
				cnt = 0
				max = 100000
				for filename in filter(lambda x:x.endswith('.xml'), os.listdir(collectionPath)):
					# print '  --', filename
					path = os.path.join (collectionPath, filename)
					rec = urlRewritingRecordClasses[xmlFormat](path=path, collection=collection)
					if rec.hasProtectedUrl():
						cnt = self.formatTally.has_key(xmlFormat) and self.formatTally[xmlFormat] or 0
						self.formatTally[xmlFormat] = cnt + 1 
						
						try:
							self.action(rec)
						except AssetNotFoundException, msg:
							if msg not in self.errors:
								self.errors.append(msg)
								
							if 1: ## quit now and debug
								print "QUITTING now to debug"
								sys.exit()
						except OSError, msg:
							pass
						
						cnt += 1
						if cnt >= max:
							break
				
							
	def default_action (self, record):
		"""
		takes no action by default
		"""
		# print ' - ', record.getProtectedUrls()[0]
		pass
		
		
	def reportFormatTally(self):
		print "Format Tally"
		lines = [];add=lines.append
		keys = self.formatTally.keys()
		keys.sort()
		cnt = 0
		for xmlFormat in keys:
			add ('- %s - %d' % (xmlFormat, self.formatTally[xmlFormat]))
			cnt += self.formatTally[xmlFormat]
		print '%d records with protected urls found' % cnt
		print '%s' % '\n'.join(lines)

def reportFormatTally():
	updater = RepoWalker (getCurriculumRepo())
	updater.reportFormatTally()

def reportMissingAssets ():
	"""
	report protected URLs in metadata that can't be resolved against 
	the asset directory
	
	setting string to True will cause asset not found exceptions to raise
	exception when assets are not found. Usually there are a few missing assets
	in the curriculum repository
	"""
	
	missing = {}
	
	def findAssets (record):
		strict = 0
		for url in record.getProtectedUrls():
			assetPath = getAssetPath(url)
			if not os.path.exists(assetPath):
				if strict:
					# raise OSError, 'Asset not found at "%s"' % assetPath
					raise Exception, 'Strict processing: Asset not found for %s at "%s"' % (record.getId(), assetPath)
				else:
					# print 'WARN: Asset not found at "%s"' % assetPath
					ids = missing.has_key(assetPath) and missing[assetPath] or []
					if record.getId() not in ids:
						ids.append(record.getId())
					missing[assetPath] = ids


	updater = RepoWalker (getCurriculumRepo(), findAssets)	
	print '\n-----------------------'
	import bscs.protected
	print ' - curriculum_view: ', bscs.protected.curriculum_view
	
	missing_assetPaths = missing.keys()
	missing_assetPaths.sort()
	print '%d missing assets' % len(missing_assetPaths)
	if len(missing_assetPaths) < 100:
		for asset_path in missing_assetPaths:
			# print "%s - %d" % (key, len(missing[key]))
			print '-',asset_path
			for recId in missing[asset_path]:
				print '   %s' % recId

def doCacheUrls(outpath="UNIQUE_URLS.txt"):
	"""
	collect unique protectedURls cataloged in the metadata, and 
	write them one per line to a file at "outpath"
	"""
	protectedUrls=[]
	
	print "doCacheUrls processing", getProtectedDir()
	
	def getUrls (record):
		for url in record.getProtectedUrls():
			if url not in protectedUrls:
				protectedUrls.append(url)
	
	updater = RepoWalker (getCurriculumRepo(), getUrls)	
	print '%d unique protectedUrls found' % len(protectedUrls)
	
	fp = open(outpath, 'w')
	protectedUrls.sort()
	fp.write ('\n'.join(protectedUrls))
	fp.close()
	print 'wrote to', outpath

def doUpdate():
	"""
	call internal "update" function on each record
	
	NOTE: bscs.protected.curriculum_view MUST be "merge".
	(this ensures that getAssetPath() will look in the OLD protectedDir)
	
	"""
	updated = []
	missing_assets = []
	existing_assets = {}
	already_existing = []
	
	def update(record):
		"""
		- rewrite all the protectedUrls in this record
		- move the cataloged assets to the new protected directory
		"""
		recordChanged = False
		
		for urlNode in record.getProtectedUrlNodes():
			url = XmlUtils.getText(urlNode)
		
			filename = os.path.basename(url)
			
			assetPath = getAssetPath (url)

			if 0:
				print '\n- assetPath:', assetPath
				print '- oldUrl:', url
				
			# Now copy the asset to new protectedDir at newAssetPath
			
			# did the protected url in metadata resolve to an existing asset?
			if not os.path.exists(assetPath):
				## Missing Asset
				# print 'asset does NOT exist at %s' % assetPath
				# raise AssetNotFoundException, assetPath
				missing_assets.append(url)
				continue
			"""
			We only want to store one copy of each asset.
			- where dups are determined by filename
			
			existing_assets holds the assets that have been written
			to the reorgProctedDir. 
			"""				
			if existing_assets.has_key(filename):
				newAssetPath = existing_assets[filename]
				# print 'asset already exists for %s:\n\t%s' % (filename, newAssetPath)
				already_existing.append(filename)
			else:
				# newAssetPath = os.path.join(getNewProtectedDir(), record.collection, filename)
				newAssetPath = os.path.join(getReorgProtectedDir(), record.collection, filename)
				
			
			# newProtectedUrl = os.path.join (base_protected_url, record.collection, os.path.basename(assetPath))
			newProtectedUrl = getProtectedUrlForPath(newAssetPath, True)

			if 0:
				print '- newProtectedUrl:', newProtectedUrl
				print '- assetPath:', assetPath
				print '- newAssetPath:', newAssetPath
				print '- DOWRITES:',dowrites

			# update the url if necessary
			if newProtectedUrl != url:
				XmlUtils.setText(urlNode, newProtectedUrl)
				recordChanged = True


			if dowrites and not os.path.exists(newAssetPath):
				
				try:
					newProtectedCollPath = os.path.dirname(newAssetPath)
					if not os.path.exists(newProtectedCollPath):
						os.mkdir(newProtectedCollPath)
				except Exception, msg:
					print 'ERROR: %s' % msg
					print ' -- newProtectedCollPath: %s' % newProtectedCollPath
					sys.exit()
					
				# copy the asset to newAssetPath
				try:
					shutil.copyfile(assetPath, newAssetPath)
					existing_assets[filename] = newAssetPath
				except OSError, msg:
					print '- ERROR: could not copy asset: %s' % msg
					print ' - assetPath: ', assetPath
					print ' - newAssetPath:', newAssetPath	
				
				print 'wrote to newAssetPath:',newAssetPath
				
			else:
				existing_assets[filename] = newAssetPath
				# print len(existing_assets.keys())
				
		# we're done with this record - write it
		if dowrites and recordChanged:
			record.write()
			# print 'wrote record for %s' % record.getId()
			
		updated.append(os.path.basename(record.path))
	
	if not dowrites:
		print "doUpdate in TEST MODE - no files are written"

	updater = RepoWalker (getReorgCurriculumRepo(), update)	
	if dowrites:
		print '%d records updated' % len(updated)
	else:
		print '%d records WOULD HAVE BEEN updated' % len(updated)
	
	print '%d errors' % len(updater.errors)
	updater.errors.sort()
	for e in updater.errors:
		print '-', e
		
	print '\n%d missing assets' % len(missing_assets)
	for a in missing_assets:
		print ' - %s' % a
		
	print '\n%d unique asset file names' % len(existing_assets.keys())
	
	print '\n%d assets collisions (asset file exists)' % len(already_existing)

if __name__ == '__main__':
	# print getMergeProtectedDir()
	if 0:
		doCacheUrls('NEW_PROTECTED_URLS.txt')
	elif 0:
		doUpdate();
	elif 0:
		print 'bscs.protected.curriculum_view: %s' % curriculum_view
		reportMissingAssets()
	elif 0:
		reportFormatTally()


	

