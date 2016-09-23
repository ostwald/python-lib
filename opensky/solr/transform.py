import lxml.etree as ET

xml_filename = '/Library/WebServer/Documents/solr/solr.xml'
xsl_filename = '/Library/WebServer/Documents/solr/solr-to-xml.xsl'

dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))
