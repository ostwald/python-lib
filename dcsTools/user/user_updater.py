import os, sys
from JloXml import MetaDataRecord, XmlUtils
from dcsTools.dcs_data import Updater, WalkingUpdater
from userRecord import UserRecord

class UserUpdater (Updater):
	"""
	instantiates a UserRecord, which can them be acted up
	"""

	verbose = 0
	
	def __init__ (self, path):
		self.user = UserRecord (path=path)
		if self.verbose:
			print self.user.getUserName()
		# here we can do something, like
		# self.userNameMappings = getUcasUserMapping (userdir)
				
	
		
class UserWalker (WalkingUpdater):
	UPDATER_CLASS = UserUpdater				
				
	def acceptDir (self, dirName):
		"""
		determine whether to visit this directory
		"""
		if dirName.lower() == 'deleted':
			return 0
		return 1

if __name__ == '__main__':
	UserWalker ("test_users")
