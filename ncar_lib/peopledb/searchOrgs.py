"""
* Get Organization Hierarchy
doc - https://wiki.ucar.edu/display/weg/Get+Organization+Hierarchy
e.g., https://api.ucar.edu/people/orgHierarchy?org=<Org Id or Org Acronym>

search params can be:
	acronym
	level
	name


returns a list of parent orgs (that can be sorted by levelCode to get hierarchy??)
Q: how does this hierarchy agree with our instDiv vocab??
"""

import os, sys, urllib, urllib2, demjson, time
from client import PeopleDBClient
from UserDict import UserDict
from ncar_lib import unionDateToSecs
from organization import Organization, org_levels

class SearchOrgs(PeopleDBClient):

	baseUrl = "https://api.ucar.edu/people"
	action = 'orgs'

	
	def __init__ (self, params):
		"""
		param can be an orgId or an Acronym
		"""
		self.params = params
		self.data = self.getData(self.action, self.params)
		self.results = map (Organization, self.data)

		
if __name__ == '__main__':
	params = {'level':'program'}
	results = SearchOrgs (params).results
	for org in results:
		print '\n',org
