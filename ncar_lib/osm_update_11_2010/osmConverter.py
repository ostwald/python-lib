"""
open a file and replace current OSM contributor element with converted form

BEFORE
<person order="1" role="Author">
      <lastName>Martinez</lastName>
      <firstName>Maribel</firstName>
      <instName>University Corporation for Atmospheric Research (UCAR)</instName>
      <instDivision>University Corporation For Atmospheric Research (UCAR):Corporate Affairs (CA)</instDivision>
      <instDivision>University Corporation For Atmospheric Research (UCAR):Corporate Affairs (CA):Education and Outreach (EO)</instDivision>
      <instDivision>University Corporation For Atmospheric Research (UCAR):Corporate Affairs (CA):Education and Outreach (EO):Significant Opportunities in Atmospheric Research and Science (SOARS)</instDivision>
      <instName2>A. Deepak Publishing</instName2>
</person>

AFTER
<person order="1" role="Author">
        <lastName>Martinez</lastName>
        <firstName>Maribel</firstName>
        <affiliation>
                <instName>University Corporation for Atmospheric Research (UCAR)</instName>
                <instDivision>
                        University Corporation For Atmospheric Research (UCAR):Corporate Affairs (CA)
                </instDivision>
                <instDivision>
                        University Corporation For Atmospheric Research (UCAR):Corporate Affairs (CA):Education and Outreach (EO)
                </instDivision>
                <instDivision>
                        University Corporation For Atmospheric Research (UCAR):Corporate Affairs (CA):Education and Outreach (EO):Significant Opportunities in Atmospheric Research and Science (SOARS)
                </instDivision>
        </affiliation>
        <affiliation>
                <instName>A. Deepak Publishing</instName>
        </affiliation>
</person>

"""
import os, sys
from JloXml import MetaDataRecord, XmlUtils
from ncar_lib.osm import OsmRecord

def convert (path, useTestSchema=True):
	
	rec = OsmRecord (path=path)
	changed = 0
	
	if useTestSchema:
		rec.setSchemaLocation('http://test.nldr.library.ucar.edu/metadata/osm/1.1/schemas/osm.xsd',
	                      'http://nldr.library.ucar.edu/metadata/osm')
	
	for contrib in rec.getContributorPeople() + rec.getContributorOrgs():
		# print "\nBEFORE\n",contrib.element.toxml()
		for level in contrib.affiliationLevels:
			suffix = contrib.getSuffix(level)
			if contrib.hasAffiliationLevel (level):
				changed=1
				affiliation = XmlUtils.addElement(rec.dom, contrib.element, 'affiliation')
				for baseFieldName in contrib.affiliationFields:
					field = baseFieldName+suffix
					child2delete = contrib.element.getElementsByTagName (field)
					if child2delete:
						for e in child2delete:
							contrib.element.removeChild (e)
					value = getattr(contrib, field)
					# print "value: '%s' (%s)" % (value, type(value))
					if value:
						if type(value) != type([]):
							value = [value]
						for item in value:
							try:
								XmlUtils.addChild (rec.dom, baseFieldName, item, affiliation)
							except TypeError:
								print "\nCouldn't insert %s in %s: %s" % (item, baseFieldName, sys.exc_info()[1])
								sys.exit()
		# print "\nAFTER\n",prettyElement(contrib.element)

	return rec
	
def prettyElement(element):
	"""
	display an element without annoying blank lines
	"""
	s = element.toprettyxml()
	lines = s.split('\n')
	return '\n'.join(filter (lambda x: x.strip(), lines))
	
if __name__ == '__main__':
	# path = 'C:/Documents and Settings/ostwald/devel/dcs-instance-data/local-ndr/records/osm/soars/SOARS-000-000-000-100.xml'
	# path = '/home/ostwald/python-lib/ncar_lib/osm_update_11_2010/test-data/osm/ams-pubs/AMS-PUBS-000-000-000-011.xml'
	osm_dir = '/home/ostwald/python-lib/ncar_lib/osm_update_11_2010/test-data/osm'
	# frag = "wos/WOS-000-000-007-102.xml"
	frag = 'osgc/OSGC-000-000-000-008.xml'
	# path = os.path.join (osm_dir, frag)
	path = 'test-OSM-record.xml'
	rec = convert (path)
	print rec
	## rec.write ("validate-me.xml")

