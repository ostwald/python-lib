"""
ORGANIZATION
# orgId: 54
# acronym: "MMM"
# name: "Mesoscale and Microscale Meteorology Division"
# level: "Division / Section"
# levelCode: 700
# parentOrg: "NESL"
"""

import os, sys
from UserDict import UserDict

# note: "program" also seems to work as a level you can search over
org_levels = [
	'Member Institution',
	'Board of Trustees',
	'UCAR',
	'Office of UCAR President',
	'Entity',
	'Directorate',
	'Lab',
	'Section',
	'Sub',
	'Group'
]

class Organization(UserDict):
	
	attrs = ['name', 'acronym', 'orgId', 'level', 'levelCode']
	
	def __init__ (self, data):
		self.data = data
		for attr in self.attrs:
			setattr(self, attr, data[attr])
			
		self.levelCode = int(self.levelCode)
			
	def __cmp__ (self, other):
		return cmp(self.levelCode, other.levelCode)
		
	def __repr__ (self):
		s=[];add=s.append
		for attr in self.attrs:
			add ('%s: %s' % (attr, getattr (self, attr)))
		return '\n'.join (s)

	def shortForm (self):
		return "%s (%s)" % (self.name, self.acronym)
		

class DetailedOrganization (Organization):
	"""
	for example of detailedOrg data see https://api.ucar.edu/people/orgs/IMAGe
	
	a few more basic attrs for the org, and then the following dicts:
		- lead (information about the lead person (e.g., upid, firstName, lastName, etc)
		- subOrgs
		- persons (information about members (same attrs as lead))
	"""
	
	attrs = Organization.attrs + ['parentOrgAcronym', 'totalHeadCount']
	
	def __init__ (self, data):
		Organization.__init__ (self, data)
		
		self.totalHeadCount = int(self.totalHeadCount)
		
		self.subOrgs = map (Organization, self.data['subOrgs'])
