"""
merge curricula

Starting point:
two repos: BSCS (src) and CCS (dst) 

A curricum merge will typically create new directories
(at xmlFormat and collection levels) but should not overwrite
any files in the dst repository

To merge curriculum (assuming all ID conflicts have been resolved):
we walk the BSCS (src) repo and copy each item-level collection into a
"relative directory" in CCS (dst) repo, creating xmlFormat and collection dirs if 
necessary.

Preparation for running curriculum merge:
- verify no conflicting item-level collections (if there are not conflicting
  collections (key/prefix), then we should never have conflicting item IDs)
-- if there are conflicting collections, use collection_tools to 
	change key and/or prefix for one of the collections
- verify no conflicting item-level IDs
- COLLECT collection - these are collection records. We don't want
to merge the master collection record from the BSCS, so we add this record's
filename to the "skip_files" list.

NOTE: after the merge, we must manually copy collection configs from src to dst as
required!

"""
import os, sys, re, shutil
from JloXml import DleseCollectRecord, XmlUtils

host = os.environ['HOST']
print "HOST", host
if host == 'acornvm':
	base_path = '/users/Home/ostwald/devel/ccs/BSCS-CCS-Merge-Data'
elif host == 'DLS-pyramid':
	base_path = '/cygdrive/c/Users/ostwald/Desktop/BSCS-CCS-Merge-Data'
elif host == 'purg.local':
	base_path = '/Users/ostwald/devel/dcs-repos/merge-workspace'
else:
	raise Exception, "host not recognized: '%s'" % host
	
BSCS_curriculum_base = os.path.join (base_path, 'dcs-bscs/records')
CCS_curriculum_base = os.path.join (base_path, 'dcs-merged/records')

dowrites = 0
verbose = 0

class DirectoryMerger:
	"""
	Merge src directory with dst directory
	"""
	skip_filenames = []
	
	def __init__ (self, src_dir, dst_dir):
		self.src_dir = src_dir
		self.dst_dir = dst_dir
		
	def acceptItem (self, filename):
		"""
		filter filenames to be merged
		"""
		if not filename.endswith('.xml'):
			return 0
		if filename in self.skip_filenames:
			return 0
		return 1
	
	def merge (self):
		"""
		wrte the items from src_dir into dst_dir
		
		collisions are reported when dowrites is False.
		when dowrites is True, collisions raise an Exception
		"""

		for filename in filter(self.acceptItem, os.listdir(self.src_dir)):
			src_path = os.path.join (self.src_dir, filename)
			dst_path = os.path.join (self.dst_dir, filename)
			
			if os.path.exists(dst_path):
				## COLLISION
				if dowrites:
					raise Exception, 'dst_path exists at %s' % dst_path
				else:  # debugging - print out collisions
					print 'COLLISION: dst_path exists at %s' % dst_path
					continue
	
			if dowrites:
				shutil.copyfile (src_path, dst_path);
			else:
				if verbose:
					print 'would have copied\n\t%s\n to\n\t%s' % (os.path.basename(src_path), dst_path)

class CollectDirectoryMerger (DirectoryMerger):
	"""
	for collection records, we have to check the COLLECTION KEY in
	the case of filename collisions
	
	skip the master collection record, since one already exists in dst

	"""
	skip_filenames = []
	
	def __init__ (self, src_dir, dst_dir):
		self.src_dir = src_dir
		self.dst_dir = dst_dir
		
	def acceptItem (self, filename):
		"""
		filter filenames to be merged
		"""
		if not filename.endswith('.xml'):
			return 0
		if filename in self.skip_filenames:
			return 0
		return 1
		
	def acceptCollectionKey (self, key):
		if key == 'collect':
			return 0
		if key.find('hsbio') != -1:
			return 0
		return 1
	
	def merge (self):
		"""
		ignore records with collection key containing 'hsbio'
		
		collisions are reported when dowrites is False.
		when dowrites is True, collisions raise an Exception
		"""
		for filename in filter(self.acceptItem, os.listdir(self.src_dir)):
			src_path = os.path.join (self.src_dir, filename)
			src_rec = DleseCollectRecord(path=src_path)
			src_key = src_rec.getKey()
			
			if not self.acceptCollectionKey(src_key):
				if verbose:
					print 'SKIPPING:', src_key
				continue
			
			dst_path = os.path.join (self.dst_dir, src_key+'.xml')
			
			if os.path.exists(dst_path):
				## COLLISION	
				if dowrites:
					raise Exception, 'dst_path exists at %s' % dst_path
				else:  # debugging - print out collisions
					print 'COLLISION: dst_path exists at %s' % dst_path
					continue
	
			if dowrites:
				src_rec.setId(src_key)
				src_rec.write(dst_path)
			else:
				if 1 or verbose:
					print 'would have copied %s to ...\n\t%s' % (os.path.basename(src_path), dst_path)

class CurriculumRepoMerger:
	"""
	merge src_repo into dst_repo
	dcs_data is merged by default (controlled with dcs_data param)
	
	Merges both collections (metadata) and collection configs (for merged collections)
	
	acceptXmlFormat and acceptCollectionKey determine which formats and collections are merged
	- collections whose key contains 'hsbil' are NOT merged.
	"""
	def __init__ (self, src_repo, dst_repo, dcs_data=1):
		self.src_repo = src_repo
		self.dst_repo = dst_repo
		self.dcs_data = dcs_data
		
		print ' - src_repo:', src_repo
		print ' - dst_repo:', dst_repo

	def getDstCollectionConfig (self, collection):
		return os.path.join (self.getDcsConf(self.dst_repo), 'collections', collection+'.xml')

	def getSrcCollectionConfig (self, collection):
		return os.path.join (self.getDcsConf(self.src_repo), 'collections', collection+'.xml')
		
	def getDcsConf (self, repo_dir):
		# print 'getDcsConf: repo_dir:', repo_dir
		
		path = os.path.join (os.path.dirname(repo_dir), 'dcs_conf')
		# print ' - ', path
		
		if not os.path.exists(path):
			raise Exception, 'DCS Conf not found at %s' % path
		return path

	
	def getDstPath (self, bscs_path):
		"""
		returns the path in the CCS repo that corresponds to the given
		path in the BSCS repo
		"""
		x = bscs_path.find (self.src_repo)
		if x != 0:
			raise IOError, "bscs_path (%s) not within self.src_repo" % bscs_path
		frag = bscs_path[len(self.src_repo)+1:]
		dst_path = os.path.join (self.dst_repo, frag)
		if not dst_path.startswith(self.dst_repo):
			raise Exception, 'getDstPath created bogus path: %s' % dst_path
		return dst_path
	
	def getDstDir (self, src_dir):
		"""
		Given a directory in the bscs repo, return the path of the corresponding
		directory in the ccs repo. Creates a CCS directory if one doesn't exist. 
		"""
		if not os.path.isdir(src_dir):
			raise Exception, 'src_dir is not a dir: %s' % src_dir
		ccs_dir = self.getDstPath (src_dir)
		if not os.path.exists(ccs_dir):
			if not dowrites:
				if 1: # debugging
					print '\t-- WARN: ccs_dir does not exist at %s' % ccs_dir
					return ccs_dir
			os.mkdir(ccs_dir)
			if verbose:
				print 'created dir at', ccs_dir
		else:
			if verbose:
				print 'ccs_dir EXISTS at %s' % ccs_dir
		return ccs_dir
		
	def getDirs (self, path):
		"""
		return the list of subdir names for given path
		"""
		return filter (lambda x:os.path.isdir(os.path.join(path, x)), os.listdir(path))
	
	def acceptCollection (self, key):
		"""
		skip all collections whose KEY contains hsbio
		"""
		return key.find('hsbio') == -1
		
	def acceptXmlFormat(self, xmlFormat):
		return xmlFormat not in ['dcs_data', 'trash']
	
	def merge (self):
		"""
		merge the two repositories unless self.dcs_data is True.
		in that case, merge the "dcs_data" directories
		
		when repositories are merged, the dcs_data is skipped
		"""
		merge_bases = [self.src_repo]
		if self.dcs_data:
			merge_bases.append(os.path.join (self.src_repo, 'dcs_data'))
			
		for merge_base in merge_bases:
			
			# for xmlFormat in filter (lambda x:x != 'dcs_data', self.getDirs(merge_base)):
			for xmlFormat in filter (self.acceptXmlFormat, self.getDirs(merge_base)):
				print '\n', xmlFormat
				xmlFormatPath = os.path.join (merge_base, xmlFormat)
				
				ccs_xmlFormatPath = self.getDstDir (xmlFormatPath)
				for collection in filter(self.acceptCollection, self.getDirs (xmlFormatPath)):
	
					print ' - ', collection
					collectionPath = os.path.join (xmlFormatPath, collection)
					ccs_collectionPath = self.getDstDir (collectionPath)
					
					if not os.path.exists(self.getDstCollectionConfig (collection)):
						if dowrites:					
							shutil.copyfile(self.getSrcCollectionConfig (collection),
											  self.getDstCollectionConfig (collection))
							print '- copied collection config for %s' % collection
						else:
							print '- WOULD HAVE copied collection config for %s' % collection
						
					if collectionPath is None:
						raise Exception, 'collectionPath is None for %s' % collection
					if ccs_collectionPath is None:
						raise Exception, 'ccs_collectionPath is None for %s' % collection
						
					if collection == 'collect':
						if merge_base.endswith('dcs_data'):
							# don't merge dcs_data for collections - CollectDirectoryMerger
							# can't handle DcsDataRecords and dcs_data for colleciton records is
							# not used (plus it is generated by DCS if it doesn't exist
							continue
						merger = CollectDirectoryMerger (collectionPath, ccs_collectionPath)
					else:
						merger = DirectoryMerger (collectionPath, ccs_collectionPath)
					merger.merge()
		
def directoryMergeTest ():
	src_dir = os.path.join (BSCS_curriculum_base, 'dcs_data', 'comm_anno/stds-nat-bscs')
	dst_dir = os.path.join (CCS_curriculum_base, 'dcs_data', 'comm_anno/stds-nat-bscs')
	merger = DirectoryMerger(src_dir, dst_dir)
	merger.merge()
	
def collectMergeTest ():
	src_dir = os.path.join (BSCS_curriculum_base, 'dlese_collect/collect')
	dst_dir = os.path.join (CCS_curriculum_base, 'dlese_collect/collect')
	merger = CollectDirectoryMerger(src_dir, dst_dir)
	merger.merge()
	
if __name__ == '__main__':
	print '\n-----------------------------------'
	if 0:
		directoryMergeTest()
	elif 0:	
		collectMergeTest()
	elif 1:
		src = BSCS_curriculum_base
		dst = CCS_curriculum_base
		merger = CurriculumRepoMerger (src, dst, dcs_data=1)
		merger.merge()
		

