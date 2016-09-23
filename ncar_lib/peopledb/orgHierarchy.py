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
from organization import Organization

class OrganizationHierarchy(PeopleDBClient):

	baseUrl = "https://people.api.ucar.edu"
	action = 'orgHierarchy'

	
	def __init__ (self, params):
		"""
		param can be an orgId or an Acronym
		"""
		self.params = params
		self.data = self.getData(self.action, self.params)
		self.parents = map (Organization, self.data)
		self.parents.sort()
		
	def asVocabString (self):
		makeSegment = lambda org: "%s (%s)" % (org.name, org.acronym)
		return ':'.join (map (makeSegment, self.parents))
		
def getOrgParents (org):
	params = {'org': org}
	# return filter (lambda x:x.levelCode >= 200, OrganizationHierarchy (params).parents)
	return OrganizationHierarchy (params).parents
		

		
	return ':'.join (map (makeSegment, parents))
		
if __name__ == '__main__':
	params = {'org':'DARES'}
	hier = OrganizationHierarchy (params)
	for org in hier.parents:
		print '\n', org
	print 'as vocab'
	print hier.asVocabString()
