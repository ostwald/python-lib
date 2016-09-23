import os, sys
from JloXml import MetaDataRecord, XmlUtils
# from dcsTools.dcs_data.walkingUpdater import Updater, WalkingUpdator
from user_updater import UserUpdater, UserWalker
from userRecord import UserRecord
from ucas_user_info import getUcasUserMapping

# userdir = "C:/Program Files/Apache Software Foundation/Tomcat 5.5/var/dcs_conf/users"
# userdir = "H:/Documents/NCAR Library/Transition to UCAS/users"

# usernameMappings = getUcasUserMapping (userdir)

# USER_NAME_MAPPINGS = None

class UcasUserUpdater (UserUpdater):
	
	USER_NAME_MAPPINGS = None
	
	def __init__ (self, path):
		if self.USER_NAME_MAPPINGS is None:
			raise KeyError, 'updater: USER_NAME_MAPPINGS not itialized'
		UserUpdater.__init__(self, path)
		print "ucas updater - %s" % self.user.getUserName()
		# here we can do something, like
		self.updateUserName()
		
	def updateUserName(self):
		username = self.user.getUserName()
		## print '\ncurrent editor: "%s"' % editor
		if self.USER_NAME_MAPPINGS.has_key (username):
			newname = self.USER_NAME_MAPPINGS[username]
			if newname != username:
				self.user.changeUserName (newname)
		
				
class UcarUserWalker (UserWalker):
	UPDATER_CLASS = UcasUserUpdater
	
	def __init__ (self, basePath):
		userNameMappings = getUcasUserMapping (basePath)

		if userNameMappings is None:
			print "walker says boo"
			raise KeyError, 'USER_NAME_MAPPINGS not itialized'
		else:
			print 'USER_NAME_MAPPINGS initialized', str(userNameMappings)
		UcasUserUpdater.USER_NAME_MAPPINGS = userNameMappings
		UserWalker.__init__ (self, basePath)

if __name__ == '__main__':
	userdir = "test_users"
	UcarUserWalker (userdir)
