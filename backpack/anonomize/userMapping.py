"""
User Mappings - generate mappings for anonomizing users
OutPut is tabdelimited file with following columns:
	['username', 'firstName', 'lastName', 'anonName']
	
this table is consulted to provide the info to anonomize (and de-anonymize if necessary), both:
	- user records
	- annotation records containing sturend names

"""
import sys, os, re
from UserDict import UserDict
from users import UserSearcher, UserInfo, makeUserInfo

class AllUsers:
	pass

class UserMappings:
	
	anonymousStudentPat = re.compile("student([\d]+)")
	skipUserNames = ['joey', 'lmelhado', 'aniess', '1student']
	
	def __init__ (self):
		self.userSearcher = UserSearcher()
		self.userInfos = map (lambda x:makeUserInfo(x.payload), self.userSearcher.data)
		self.userInfos.sort()
		self.userMap = self.initUserMap()
		self.nextIndex = self.initIndex()
		
	def initIndex (self):
		max_index = 0
		for key in self.userMap.keys():
			m = self.anonymousStudentPat.match(key)
			if m:
				# print m.group(1)
				max_index = max(int(m.group(1)), max_index)
		return max_index+1
		
	def initUserMap(self):
		userMap = UserDict()
		for userInfo in self.userSearcher:
			userMap[userInfo.username] = userInfo
		return userMap

	def writeUserMappings (self, path=None):
		"""
		make tab delimited file of mappings
		"""
		lines=[];add=lines.append
		hdr = ['username', 'firstName', 'lastName', 'anonName']
		add (hdr)
		for result in um.userSearcher:
			if 'teacher' in result.roles:
				m = self.anonymousStudentPat.match(result.username)
				if m or result.username in self.skipUserNames:
					continue # this one is alread anonomized
				anonName = 'student%d' % self.nextIndex
				self.nextIndex += 1
				add ([result.username, result.firstName, result.lastName, anonName])
		data = '\n'.join (map (lambda x:'\t'.join(x), lines))
		print data
		if not path:
			path = "USER_MAPPINGS.txt"
		fp = open(path,'w')
		fp.write(data)
		fp.close()
		print 'wrote mappings to', path
		
def userSearcherTester ():
	searcher = UserSearcher()
	for result in searcher:
		print result.payload.report()
		
if __name__ == '__main__':
	um = UserMappings()
	um.writeUserMappings()

