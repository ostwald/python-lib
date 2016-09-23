"""
Merge one User Content repository (src) into another (dst).

User Content repos usually have identical directory structures (the formats,
and collections are the same), and the merge process is writing the item-level
metadata from the src (e.g., BSCS) repo into the like-named collections in the dst
repo (e.g., CCS).

Because the src and dst collections are the same, we don't merge the collection
of collection records (dlese_collect/collect).

Because we are writing records from src to existing dst collections, the risk
of item-level ID collisions is present (especially since many of the filenames
are system-generated). Make sure and verify that there are no ID collisions
throughout the repository. NOTE: currently, ID collisions are reported, but the
record in the destination directory is not overwritten.

IMPLEMENTATION
CollectionMerger and UserCollectionMerger merge a single collection.

UserContentMerger merges the repositories by making repeated calls to
CollectionMerger and UserCollectionMerger.merge().


see bscs_user_content_workflow.py for users of this module
	e.g., merge bscs user content repo into a ccs user content repo
"""
import os, sys, re, shutil

class CollectionMerger:
	"""
	CollectionMerger takes two directores, src_dir and dst_dir, and
	merges src into dest.
	
	In test mode (test=True) no files are written
	"""
	
	skipfiles = []
	
	def __init__ (self, src_dir, dst_dir, test=0):
		self.src_dir = src_dir
		self.dst_dir = dst_dir
		if not (os.path.basename(self.src_dir) == os.path.basename(self.dst_dir)):
			raise Exception, "src and dst dirs must have the same basename"
		self.test = test
		self.src_paths = self.get_paths(self.src_dir)
		self.dst_paths = self.get_paths(self.dst_dir)

	def accept_file(self, path):
		if os.path.isdir(path):
			return 0
		filename = os.path.basename(path)
		if not filename.endswith('.xml'):
			return 0
		return 1
		
	def get_paths (self, mydir):
		return  filter (self.accept_file, 
						map (lambda x:os.path.join (mydir, x),
							 os.listdir(mydir)))
		
	def merge(self):
		"""
		cp the files in src_dir into dst_dir

		collision -when there are matching files both directories, and the src
		file collides with its counter part in dest_dir.
		
		merge records collisions, but does not overwrite dst file
		"""
		collisions=[]
		if self.test:
			print 'merge_collections: %s' % os.path.basename(self.src_dir)
			print ' - src has %d files' % len (self.src_paths)
			print ' - dst has %d files' % len (self.dst_paths)
	
		for src in self.src_paths:
			filename = os.path.basename(src)
			dst = os.path.join (self.dst_dir, filename)
			if os.path.exists(dst):
				if self.test:
					print filename, ' exists in dst dir'
					collisions.append (filename)
				continue
				
			if not self.accept_file(src):
				raise Exception, 'UNACCEPTABLE: %s' % src
				
			if not self.test:
				shutil.copyfile(src, dst)
			else:
				print ' - would have copied', filename
		if self.test:
			print '  .. done merging %s - %d collisions' % (os.path.basename(self.src_dir), len(collisions))

class UserCollectionMerger (CollectionMerger):
	"""
	A CollectionMerger specialized to operate over USER records.
	
	userIds_to_ignore - userIds that were found to have username conflicts
	with the CCS user_content repository (see __init__.py, dup_users.py).
	"""
	
	def __init__ (self, src_dir, dst_dir, userIds_to_ignore=None, test=0):
		self.skipfiles = map (lambda x:x+'.xml', userIds_to_ignore)
		CollectionMerger.__init__(self, src_dir, dst_dir, test)
		
	def accept_file(self, path):
		if os.path.isdir(path):
			return 0
		filename = os.path.basename(path)
		if filename in self.skipfiles:
			print 'Skipping ', filename
			return 0
		if not filename.endswith('.xml'):
			return 0
		return 1
		


class UserContentMerger:
	"""
	Takes two User Content repsitories and merges the item-level metadata
	from src_repo into dst_repo.
	
	"""
	skip_collections = []
	skip_xmlFormats = ['dlese_collect']
	
	def __init__(self, src_repo, dst_repo, userIds_to_ignore=None, test=None):
		"""
		src_repo is merged into dst_repo
		"""
		self.src_repo = src_repo
		self.dst_repo = dst_repo
		self.userIds_to_ignore = userIds_to_ignore
		self.test = test

		
	def merge (self):
		print 'CollectionMerger merge'

		for xmlFormatPath in self.get_dirs(self.src_repo):
			xmlFormat = os.path.basename(xmlFormatPath);
			print ' -', xmlFormat
			if xmlFormat in self.skip_xmlFormats:
				print ' -- SKIPPED'
				continue	
			# print '  ', self.getDestPath(xmlFormatPath)
			for collectionPath in self.get_dirs(xmlFormatPath):
				collection = os.path.basename(collectionPath)
				print '   -', collection
				if collection == 'ccsusers':
					coll_merger = UserCollectionMerger(collectionPath, self.getDestPath(collectionPath), self.userIds_to_ignore, self.test)
				elif collection in self.skip_collections:
					continue
				else:
					coll_merger = CollectionMerger(collectionPath, self.getDestPath(collectionPath), self.test)
				coll_merger.merge()
	
	def accept_dir(self, path):
		if not os.path.isdir(path):
			return 0
		dirname = os.path.basename(path)
		if dirname[0] == '.':
			return 0
		if dirname == 'svn':
			return 0
		return 1

	def getDestPath (self, src_path):
		# print 'getDestPath: "%s"' % src_path
		if not src_path.find (self.src_repo) == 0:
			raise Exception, 'src_path is not within src_repo (%s)' % self.src_repo
		dst_path = src_path.replace(self.src_repo, self.dst_repo) 
		if not os.path.exists(dst_path):
			raise Exception, 'dst_path does not exist at "%s"' % dst_path
		return dst_path
		
	def get_dirs(self, parent_dir):
			return  filter (self.accept_dir, 
							map (lambda x:os.path.join (parent_dir, x),
								 os.listdir(parent_dir)))			 

if __name__ == '__main__':
	# see bscs_user_content_workflow.py for users of this module
	pass
