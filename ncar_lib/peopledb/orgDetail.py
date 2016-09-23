"""
* Get Organization Hierarchy
doc - https://wiki.ucar.edu/display/weg/Get+Organization+Hierarchy
e.g., https://api.ucar.edu/people/orgHierarchy?org=<Org Id or Org Acronym>

returns a list of parent orgs (that can be sorted by levelCode to get hierarchy??)
Q: how does this hierarchy agree with our instDiv vocab??
"""

import os, sys, urllib, urllib2, demjson, time
from client import PeopleDBClient
from UserDict import UserDict
from ncar_lib import unionDateToSecs
from organization import Organization, DetailedOrganization

class OrgDetailClient(PeopleDBClient):

	baseUrl = "https://people.api.ucar.edu/orgs"
	action = None

	
	def __init__ (self, query):
		"""
		param can be an orgId or an Acronym
		"""
		self.query = query
		self.orgDetails = None
		try:
			self.data = self.getData(action=query)
			print self.data
			self.org = DetailedOrganization (self.data)
		except:
			print "org not found for %s" % self.query
			self.data = None
			
		
			
	def getUrl (self, action, params):
		url = self.baseUrl
		if action:
			url = os.path.join (self.baseUrl, action)
		if params:
			url += "?" + self.paramsToQueryString(params)
		# print url
		return url		

def getOrganizationDetails (org):
	return OrgDetailClient (org).org
		
if __name__ == '__main__':
	q = 'image'
	client = OrgDetailClient (q)
	print client.org
	print 'SUBORGS'
	for sub in client.org.subOrgs:
		print sub.shortForm()

