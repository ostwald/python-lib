import lxml

import lxml.etree as ET

def transform (xml_path, xsl_path):
	dom = ET.parse(xml_path)
	xslt = ET.parse(xsl_path)
	xform = ET.XSLT(xslt)
	return xform(dom)

def transform_tree (dom, xsl_path):
	xslt = ET.parse(xsl_path)
	xform = ET.XSLT(xslt)
	return xform(dom)

