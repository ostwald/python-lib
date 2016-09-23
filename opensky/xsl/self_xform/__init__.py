"""
self-transform path on Clone: sites/all/modules/islandora_xml_forms/builder/self_transforms/
"""
from opensky.xsl import transform, ET

xml = 'mods_1.xml'
xsl = 'cleanup_mods.xsl'
# # xsl = 'islandora_cleanup_mods_extended.xsl'
#
# # xml = 'no-ns.xml'
# # xsl = 'no-ns.xsl'

transformed = transform(xml, xsl)

print(ET.tostring(transformed, pretty_print=True))