import os, sys, re
from UserList import UserList
# from HyperText.HTML import *
from user_info import User, Users 
from dcsTools.dcs_data import nsdlToLdap_Globals


"""
Simple reader for DCS User records (using regular expressions)
"""


## userdir = "C:/Program Files/Apache Software Foundation/Tomcat 5.5/var/dcs_conf/users"
## userdir = "H:/Documents/NSDL/TransitionToLdap/ncs-users-2009-11-02"

# userdir = "H:/Documents/NCAR Library/Transition to UCAS/users"

def findTag (s, tag):
	pat = re.compile ("<%s>(.*?)</%s>" % (tag, tag), re.DOTALL | re.MULTILINE)
	m = pat.search (s)
	if m:
		return m.group(1).strip()
	else:
		return None

class LdapUser (User):

	def makePeopleDBLink (self):
		# baseUrl = 'https://api.ucar.edu/people/internalPersons?lastName=%s' % self.lastname
		## baseUrl = 'https://api.ucar.edu/people/internalPersons?email=%s' % self.email
		baseUrl = 'https://api.ucar.edu/people/internalPersons?email=%s' % self.email
		return baseUrl
		
		
			
class LdapUsers (Users):
		
	def __init__ (self, dirname):
		Users.__init__ (self, dirname)

	def getLdapUserMapping (self):
		"""
		consult a mapping table
		"""
		from xls import XslWorksheet, WorksheetEntry
		table = XslWorksheet ()
		table.read (nsdlToLdap_Globals.USERNAME_XLS)
		mapping = {}
		for rec in table:
			username = rec['username']
			# print "%s (%s)" % (username, rec['ldap acccount'])
			if username in mapping.keys():
				raise KeyError, "duplicate entry for '%s'" % username
			mapping[username] = rec['ldap acccount']
		return mapping
		

def getLdapUserMapping (dirname):
	# return {'jonathan': 'ostwald'}
	return LdapUsers(dirname).getLdapUserMapping()
		
if __name__ == '__main__':
	# print UcarUsers(userdir).toTabDelimited()
	# UcarUsers(userdir).toPeopleDBQueries()
	userdir = 'test_users'
	print getLdapUserMapping(userdir)
