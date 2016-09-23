import os, sys, re
from UserList import UserList
from HyperText.HTML import *
from user_info import User, Users 

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

class UcasUser (User):

	def makePeopleDBLink (self):
		# baseUrl = 'https://api.ucar.edu/people/internalPersons?lastName=%s' % self.lastname
		## baseUrl = 'https://api.ucar.edu/people/internalPersons?email=%s' % self.email
		baseUrl = 'https://api.ucar.edu/people/internalPersons?email=%s' % self.email
		return baseUrl
		
		
			
class UcasUsers (Users):
		
	def __init__ (self, dirname):
		Users.__init__ (self, dirname)

	def toPeopleDBQueries (self):
		"""
		create html links against the UCAR peopleDB for each user
		"""
		writeToFile = 1

		container = DIV()
		
		for user in self:
			linktext = "%s %s (%s)" % (user.firstname, user.lastname, user.username)
			href = Href (user.makePeopleDBLink(), linktext)
			container.append (DIV (href, style="margin:5px"))

		if writeToFile:
			outpath = os.path.join (os.path.dirname (self.dirname),
									 "peopleQueries.html")
			print "outpath: %s" % outpath
			fp = open (outpath, 'w')
			fp.write (container.__str__())
			fp.close()
		else:
			print container

	def makeUcasUserMappingTxt (self):
		"""
		create a python mapping from DCS username to Ucas username
		"""

		s=[];add=s.append
		vals = []
		for user in self:
			email = user.email
			if email:
				val = email.split('@')[0]
			else:
				val = None
			if val:
				add ("'%s' : '%s'" % (user.username, val))

		return 'ucasUserMapping = {\n\t%s\n}' % ',\n\t'.join(s)

	def getUcasUserMapping (self):
		"""
		create a python mapping from DCS username to Ucas username
		Useful when we want to change current to new usernames to match auth scheme
		"""
		mapping = {}
		for user in self:
			email = user.email
			if email:
				val = email.split('@')[0]
			else:
				val = None
			if val:
				mapping[user.username] = val
		return mapping

def getUcasUserMapping (dirname):
	return UcasUsers(dirname).getUcasUserMapping()
		
if __name__ == '__main__':
	# print UcarUsers(userdir).toTabDelimited()
	# UcarUsers(userdir).toPeopleDBQueries()
	userdir = 'test_users'
	print getUcasUserMapping(userdir)
