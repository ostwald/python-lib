"""
self-transform path on Clone: sites/all/modules/islandora_xml_forms/builder/self_transforms/
"""
from opensky.xsl import transform, ET

if __name__ == '__main__':
	xml = '/Users/ostwald/Downloads/articles18555_cloneDOI+testmasterIIINoSelfTrans.xml'
	# xsl = 'cleanup_mods.xsl'
	xsl = '/Users/ostwald/devel/github/libroot/utils/osm/xslt/opensky/ncarcleanup_mods.xsl'
	# # xsl = 'islandora_cleanup_mods_extended.xsl'
	#
	# # xml = 'no-ns.xml'
	# # xsl = 'no-ns.xsl'

	print '*'*80
	print "self transform"
	print ' - XML:',xml
	print ' - TRANSFORM:',xsl
	print '\n'

	transformed = transform(xml, xsl)

	print(ET.tostring(transformed, pretty_print=True))