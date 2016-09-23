"""
protected_urls - reads and reports contents of "unique_urls" file that is created by
curriculum_reorg_tools

Attributes
- unique_asset_names
- ccs_urls
- bscs_urls
- dps_urls
- num_dups

"""
import os, sys, re
from UserList import UserList
from bscs.protected import isBscsProtectedUrl, isCcsProtectedUrl, isAnyProtectedUrl, isDpsProtectedUrl

class ProtectedUrls (UserList):
	
	def __init__ (self, url_data_path):
		self.data_path = url_data_path
		self.name = os.path.basename(self.data_path)
		content = open(self.data_path, 'r').read()
		self.data = filter(None, map(lambda x:x.strip(), content.split('\n')))
		
		self.unique_asset_names = []
		self.dups = {}
		for url in self:
			filename = os.path.basename(url)
			if filename not in self.unique_asset_names:
				self.unique_asset_names.append(filename)
			else:
				cnt = self.dups.has_key(filename) and self.dups[filename] or 0
				self.dups[filename] = cnt + 1
				
		self.dup_cnt = 0 # count the urls that do not count towards unique filenames
		for key in self.dups.keys():
			self.dup_cnt += self.dups[key]

		self.bscs_urls = filter (lambda x:isBscsProtectedUrl(x),	self)
		self.ccs_urls = filter (lambda x:isCcsProtectedUrl(x), self)
		self.dps_urls = filter (lambda x:isDpsProtectedUrl(x), self)


	def report (self):
		
		print '\nreporting over ProtectedUrls ...'
				
		print ' .. out of a total %d unique Urls' % len (self)
		print "- %d unique asset names found in uniqueUrls" % len(self.unique_asset_names)
		print "- %d asset names were not unique" % len(self.dups.keys())
		print '- %d total dup asset names found' % self.dup_cnt
		
		print '\nUnique plus dups: %d' % (len(self.unique_asset_names) + self.dup_cnt)
		
		self.bscs_urls = filter (lambda x:isBscsProtectedUrl(x),	self)
		self.ccs_urls = filter (lambda x:isCcsProtectedUrl(x), self)
		self.dps_urls = filter (lambda x:isDpsProtectedUrl(x), self)
		all_urls = filter (lambda x:isAnyProtectedUrl(x), self)
		
		print '\n%d bscsProtectedUrls' % len(self.bscs_urls)
		print '%d ccsProtectedUrls' % len(self.ccs_urls)
		print '%d dpsProtectedUrls' % len(self.dps_urls)
		
		accounted_for_urls = self.bscs_urls + self.ccs_urls + self.dps_urls
		if len(accounted_for_urls) != len(self):
			print "WARN: %d unaccounted for urls" % (len(self) - len (accounted_for_urls))
			for url in accounted_for_urls:
				print '-', url
		else:
			print "Success: No accounted_for_urls"
			
class ProtectedUrlsCompare:
	
	def __init__ (self, data_path_1, data_path_2):
		self.urls_1 = ProtectedUrls (data_path_1)
		self.urls_2 = ProtectedUrls (data_path_2)
		
		print '- 1 - %s has %d protectedUrls, %d unique asset names' % (self.urls_1.name, len(self.urls_1), len(self.urls_1.unique_asset_names))
		print '- 2 - %s has %d protectedUrls, %d unique asset names' % (self.urls_2.name, len(self.urls_2), len(self.urls_2.unique_asset_names))
		
		print ''
		self.compare(self.urls_1, self.urls_2)
		self.compare(self.urls_2, self.urls_1)
		
		if 0: # not meaningful to compare full urls
			print ''
			self.compareFullUrls(self.urls_1, self.urls_2)
			self.compareFullUrls(self.urls_2, self.urls_1)
		
	def compare (self, urls_a, urls_b):		
		a_asset_names = urls_a.unique_asset_names
		a_asset_names.sort()
		b_asset_names = urls_b.unique_asset_names
		b_asset_names.sort()
		extra = filter (lambda x:x not in b_asset_names, a_asset_names)
		print "%d asset_names in %s but not in %s" % (len(extra), urls_a.name, urls_b.name)
		for asset_name in extra:
			# print '-', asset_name
			pass
	
	def compareFullUrls (self, urls_a, urls_b):		

		extra = filter (lambda x:x not in urls_b, urls_a)
		print "%d urls in %s but not in %s" % (len(extra), urls_a.name, urls_b.name)
		for asset_name in extra:
			# print '-', asset_name
			pass
		
if __name__ == '__main__':
	ProtectedUrlsCompare ('MERGE_UNIQUE_URLS.txt', 'REORG_UNIQUE_URLS.txt')
		
