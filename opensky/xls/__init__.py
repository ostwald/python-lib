import lxml

import lxml.etree as ET

xml = 'mods_1.xml'
# xsl = 'cleanup_mods.xsl'
xsl = 'islandora_cleanup_mods_extended.xsl'

# xml = 'no-ns.xml'
# xsl = 'no-ns.xsl'

dom = ET.parse(xml)
xslt = ET.parse(xsl)
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))