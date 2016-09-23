"""
look over the records changed already and look for MULTIPLE-AFFILIATIONS
- for each author, count affiliations
"""

import sys, os
from ncar_lib.osm.osmRecord import OsmRecord, Affiliation

records_base = "records"
osgc_dir = os.path.join (records_base, 'osgc')

for filename in os.listdir (osgc_dir):
	if not filename.endswith('.xml'): continue
	path = os.path.join (osgc_dir, filename)
	rec = OsmRecord (path=path)
	authors = rec.getContributorPeople()
	print rec.getId()
	for author in authors:
		affiliations = map (Affiliation, author.getAffiliationElements())
		print ' - %s (%d)' % (author.lastName, len(affiliations))
		

