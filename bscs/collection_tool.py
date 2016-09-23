"""
CollectionTool

Supports changing the collection key and metadata prefix for a collection

Changing the prefix for a collection entails:

- changePrefix() - Update all metadata with new Ids (NewId = OldId.replace(oldPrefix, newPrefix)
  - change ID inside metadata
  - rename file with new Id+'.xml'
- updateCollectionConfig() - Update collection config (which specifies the prefix)

Changing the collection key entails:

- updateCollectionDirName() - rename the directory holding metadata and dcs_data for this collection
- updateCollectionConfig() - Update collection config file
  - change collection key in config xml
  - rename file for newKey.xml
- updateCollectionRecord() - Update the collection record for this collection (newKey)

"""
import os, sys, re, shutil
from JloXml import XmlRecord, XmlUtils, DleseCollectRecord, CollectionConfigRecord

class CollectionTool:
	"""
	a collection must have its id_path registered on id_paths to update
	item level metadata
	"""
	id_paths = {
		'comm_anno' : 'comm_anno:recordID',
		'dcs_data' : 'dcsDataRecord:recordID'
	}
	
	dowrites = 0
	repo_type = 'DCS' # 'DDS'
	
	def __init__ (self, repo, xmlFormat, key):
		"""
		CollectionTools are defined for a collection, which is determined
		by repo, xmlFormat, and collection key
		"""
		print 'CollectionTool repo: ' + repo
		self.repo = repo
		self.xmlFormat = xmlFormat
		self.key = key
		
	def testXmlFormat(self):
		"""
		raises an error if this collection's format is not implemented
		"""
		if not self.id_paths.has_key(self.xmlFormat):
			raise KeyError, 'xmlFormat "%s" not recognized' % self.xmlFormat
		
		
	def changePrefix (self, old_prefix, new_prefix):
		"""
		Update the record id and rename the metdata files for this collection
		(both item level metadata and dcs_data metadata)
		"""
		print 'changePrefix old: %s, new: %s' % (old_prefix, new_prefix)
		
		try:
			self.testXmlFormat()
		except KeyError, msg:
			raise Exception, "ERROR cannot change prefix: %s", msg
		
		rel_paths = ['%s/%s' % (self.xmlFormat, self.key)]
	
		if self.repo_type == 'DCS':
			rel_paths.append('dcs_data/%s/%s' % (self.xmlFormat, self.key))
	
		# for frag in ['dcs_data/comm_anno/'+self.key, 'comm_anno/'+self.key]:
		for frag in rel_paths:
			collection = os.path.join (self.repo, frag)
			filenames = filter (lambda x:x.endswith('.xml'), os.listdir(collection))
			print '%d files in %s' % (len(filenames), frag)
			
			for path in map(lambda x:os.path.join (collection, x), filenames):
				rec = XmlRecord(path=path)
				
				# update the recordId
				if frag.startswith('dcs_data'):
					idpath = 'dcsDataRecord:recordID'
				else:
					idpath = self.id_paths[self.xmlFormat]
				id = rec.getTextAtPath(idpath)
				newId = id.replace (old_prefix, new_prefix)
				rec.setTextAtPath(idpath, newId)
				
				newPath = os.path.join (collection, newId+'.xml')
				if self.dowrites:
					# write new record and remove the old one
					rec.write(newPath)
					print 'wrote to', newPath
					os.remove(path)
				else:
					print 'WOULD have written to', newPath
			
	def updateCollectionDirName (self, new_key):
		item_dir_path = os.path.join (self.repo, self.xmlFormat, self.key)
		new_item_dir = os.path.join (self.repo, self.xmlFormat, new_key)
		
		dcs_data_dir_path = os.path.join (self.repo, 'dcs_data', self.xmlFormat, self.key)
		new_dcs_data_dir_path = os.path.join (self.repo, 'dcs_data', self.xmlFormat, new_key)
			
		if self.dowrites:
			os.rename(item_dir_path, new_item_dir)
			print '- renamed item dir to %s' % os.path.basename(new_item_dir)
			if self.repo_type == 'DCS':
				os.rename(dcs_data_dir_path, new_dcs_data_dir_path)
				print '- renamed dcs_data dir to %s' % os.path.basename(new_item_dir)
		else:
			if not os.path.exists(item_dir_path):
				raise Exception, 'item_dir_path does not exist at "%s"' % item_dir_path
			if self.repo_type == 'DCS' and not os.path.exists(item_dir_path):
				raise Exception, 'dcs_data_dir_path does not exist at "%s"' % item_dir_path
			print '- WOULD HAVE item directory dirs to %s' % os.path.basename(new_item_dir)

			
	def updateCollectionRecord(self, new_key, new_name=None):
		"""
		- find the collection record with this collections prefix
		  -- we look through them one by one
		- update the prefix
		- if dowrites:
		  - write collection record
	  """
		collect = os.path.join (self.repo, "dlese_collect", "collect")
		for filename in filter (lambda x:x.endswith('xml'), os.listdir(collect)):
			# print filename
			path = os.path.join(collect, filename)
			rec = DleseCollectRecord(path=path)
			oldKey = rec.getKey()
			if oldKey == self.key:
				print 'old key: %s' % rec.getKey()
				rec.setKey(new_key)
				rec.setId(new_key)
				if new_name:
					rec.setShortTitle (new_name)
					rec.setFullTitle(new_name)
				
				if self.dowrites:
					rec.write()
					os.rename(path, os.path.join(collect, new_key+'.xml'))
					print 'wrote collection record: %s' % rec.getId()
				else:
					print rec
					print 'WOULD have written collection record: %s' % rec.getId()
				return
				
	def updateCollectionConfig (self, collection_config_dir, new_key=None, new_prefix=None):
		"""
		- collection_config_dir - e.g., ..../dcs_conf/collections
		- new_key - the key the updated collection will have
		- new_prefix - the metadata prefix the updated collection will have
		"""
		
		config_path = os.path.join (collection_config_dir, self.key+'.xml')
		if not os.path.exists(config_path):
			raise Exception, 'ConfigFile not found at "%s"' % config_path
		rec = CollectionConfigRecord (config_path)
		
		if new_prefix is not None:
			rec.setIdPrefix (new_prefix)
		if new_key is not None:
			rec.setKey(new_key)
		if self.dowrites:
			rec.write()
			print 'wrote', config_path
		if new_key != self.key:
			new_config_path = os.path.join(os.path.dirname(config_path), new_key+'.xml')
			if self.dowrites:
				os.rename(config_path, new_config_path)
				print 'Renamed config to', os.path.basename(new_config_path)
			else:
				print rec
				print 'WOULD have renamed config to', os.path.basename(new_config_path)

