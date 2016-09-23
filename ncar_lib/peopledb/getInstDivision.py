"""
given an acronym, return the vocab value for instDiv

1 - find organization
2 - find parents

concat org.name (org.acronym) for parents until levelCode < 200

"""

import os, sys, urllib, urllib2, demjson, time
from client import PeopleDBClient
from UserDict import UserDict
from ncar_lib import unionDateToSecs
from organization import Organization
from orgDetail import getOrganizationDetails
from orgHierarchy import getOrgParents


def getVocabSegment (org):
	return "%s (%s)" % (org.name, org.acronym)


def getInstDivisionVocab (org):
	"""
	org can be an acronym or orgId
	"""
	myorg = getOrganizationDetails (org)
	if myorg is None:
		raise Exception, 'Org not found for %s' % org
		
	parents = getOrgParents (org)
	# filter out upper orgs
	parents = filter (lambda x:x.levelCode >= 200, parents)
	parents.append (myorg)
	
	return ':'.join(map (getVocabSegment, parents))
		
		
if __name__ == '__main__':
	org = 'NCAR'
	print getInstDivisionVocab (org)
