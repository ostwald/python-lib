"""
UserInfoSet - extends IdSet to compare userNames, rather than recordIds

data files read by UserInfoSet have on entry per line:
 - 1247065132457	ostwald
      userId         username

- compareNames - find usernames in this UserInfoSet that not in the other UserInfoSet

- inCommonNames - find usernames in this UserInfoSet that are also in the other UserInfoSet
"""
import os, sys, string
from dataset import DataSet
from UserDict import UserDict
from idset import IdSet

class UserInfoSet (IdSet):
	def __init__ (self, filename, dataSetName):
		"""
		Beyond IdSets functionality, provides for 
		detecting username collisions
		"""
		IdSet.__init__ (self, filename, dataSetName)
		self.idhash, self.namehash = self.makeHashes()
		
		self.names = self.namehash.keys()
		self.names.sort()
		
		
	def makeHashes(self):
		"""
		create to hashes to access this UserInfoSet's ids:
		- idhash - id -> username
		- namehash - username -> id
		"""
		idhash = UserDict()
		namehash = UserDict()
		for entry in self:
			splits = map(string.strip, entry.split('\t'))
			idhash[splits[0]] = splits[1]
			namehash[splits[1]] = splits[0]
		return idhash, namehash
	
	def compareNames (self, other):
		"""
		find usernames in this UserInfoSet that not in the other UserInfoSet
		"""
		missing = filter (lambda x:x not in other.names, self.names)
		print 'there are %d names in %s that are NOT in %s' % (len(missing), self.title, other.title) 

	def inCommonNames (self, other):
		"""
		find usernames in this UserInfoSet that are also in the other UserInfoSet
		"""
		common = filter (lambda x:x in other.names, self.names)
		print 'there are %d names that are in both idSets' % len(common) 
		return common		

def userInfoReport():
	filename = 'userInfo.txt'
	infoset1 = UserInfoSet(filename, 'BSCS')
	infoset2 = UserInfoSet(filename, 'CCS')
	
	commonNames = infoset1.inCommonNames(infoset2)
	#printlist(commonNames)
	for name in commonNames:
		set1id = infoset1.namehash[name]
		set2id = infoset2.namehash[name]
		print '%s - %s - %s' % (name, set1id, set2id)
	
	# infoset1.compareNames(infoset2)
	# infoset2.compareNames(infoset1)
		
def printlist(list, title=None):
	if title:
		print title
	for item in list:
		print '- ', item
		
if __name__ == '__main__':
	
	userInfoReport()
