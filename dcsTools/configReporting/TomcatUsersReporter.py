"""
	FileTools - classes to support working with the various files
	associated with a DcsInstance
"""

import sys, os, site, string
if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")
					 
from PathTool import localize
from JloXml import XmlRecord
from dcsTools.instanceWalker import InstanceWalker, DcsInstance
				
class User:
	"""
	class encapsulating a user as defined in a tomcat-users.xml file
	"""
	
	def __init__ (self, userElement):
		self.element = userElement
		self.username = userElement.getAttribute ("username")
		self.password = userElement.getAttribute ("password")
		self.roles = userElement.getAttribute ("roles")
		
	def __repr__ (self):
		return "User: %s  Password: %s  Roles: %s" % (self.username, self.password, self.roles)

class TomcatUsersReporter (XmlRecord):

	def __init__ (self, instance):
		self.instance = instance
		XmlRecord.__init__ (self, path=instance._get_tomcat_users_path())
		self.users = self._get_users()
	
	def _get_users (self):
		"""
		selects the elements defining users from the tomcat-users file
		"""
		users = []
		user_elements = self.getElementsByXpath (self.dom, "tomcat-users:user")
		for e in user_elements:
			users.append (User (e))
		return users
		
	def report (self):
		print ("TomcatUsersReporter")
		for user in self.users:
			print ("\t%s" % str(user))
			
	def report_user (self, username):
		for u in self.users:
			if u.username == username:
				print "\t%s" % u
		
## -------------------------------------------------------------
##
##  TomcatUsersReporter applications
##


def tomcat_user_report (instance):
	"""
	report on the tomcat-users file for given instance
	
	as call-back for walker, must take a DcsInstance as input
	"""
	print "%s\n Tomcat Users Report for %s\n" % ("-"*50, string.upper (instance.name))
	tool = TomcatUsersReporter (instance)
	# see content of tomcat-users file
	# print tool
	tool.report()
	
def tomcat_single_user_report (instance):
	"""
	report on the tomcat-users file for given instance
	
	as call-back for walker, must take a DcsInstance as input
	"""
	print "%s\n Tomcat Users Report for %s\n" % ("-"*50, string.upper (instance.name))
	tool = TomcatUsersReporter (instance)
	# see content of tomcat-users file
	username = "dcs"
	tool.report_user (username)

		
# report on all instances
def tomcat_user_walker (baseDir, fn):	
	"""
	run function on all instances
	"""
	InstanceWalker (baseDir).walk (fn)	
		
## --------------------------------------------------------
	
def show_users_stuff ():
	instancepath = localize ("/export/services/dcs/dcs.dlese.org/tomcat/noaa")
	instance = DcsInstance (instancepath)
	show_user_stuff (instance)

if __name__ == "__main__":
	baseDir = localize ("/export/services/dcs/dcs.dlese.org/tomcat")
	
	## show_users_stuff ()
	
	# report on all users
	# tomcat_user_walker (baseDir, tomcat_user_report)
	
	# report on single users (specified in call_back)
	tomcat_user_walker (baseDir, tomcat_single_user_report)




