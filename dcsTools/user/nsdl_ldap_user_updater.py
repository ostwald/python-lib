import os, sys
# from JloXml import MetaDataRecord, XmlUtils
# from dcsTools.dcs_data.walkingUpdater import Updater, WalkingUpdator
from user_updater import UserUpdater, UserWalker
# from userRecord import UserRecord
from nsdl_ldap_user_info import getLdapUserMapping
from dcsTools.dcs_data import nsdlToLdap_Globals


class LdapUserUpdater (UserUpdater):
	
	USER_NAME_MAPPINGS = None
	verbose = 0
	
	def __init__ (self, path):
		if self.USER_NAME_MAPPINGS is None:
			raise KeyError, 'updater: USER_NAME_MAPPINGS not itialized'
		UserUpdater.__init__(self, path)
		if self.verbose:
			print "Ldap updater - %s" % self.user.getUserName()
		# here we can do something, like
		self.updateUserName()
		
	def updateUserName(self):
		username = self.user.getUserName()
		## print '\ncurrent editor: "%s"' % editor
		if self.USER_NAME_MAPPINGS.has_key (username):
			newname = self.USER_NAME_MAPPINGS[username]
			if '?' in newname:
				return
			if newname != username:
				if 1 or self.verbose:
					print '%s --> %s' % (username, newname)
				self.user.changeUserName (newname)
		
				
class LdapUserWalker (UserWalker):
	UPDATER_CLASS = LdapUserUpdater

	def __init__ (self, basePath):
		userNameMappings = getLdapUserMapping (basePath)

		if userNameMappings is None:
			raise KeyError, 'USER_NAME_MAPPINGS not itialized'

		LdapUserUpdater.USER_NAME_MAPPINGS = userNameMappings
		UserWalker.__init__ (self, basePath)

if __name__ == '__main__':
	# userdir = "test_users"
	userdir = nsdlToLdap_Globals.USER_DATA_DIR
	LdapUserWalker (userdir)
