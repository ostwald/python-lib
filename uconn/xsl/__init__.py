"""
We're looking for this kind of thing:

	<xsl:if test="contains($allresourceTypes, 'Calculation or conversion tool')">
		<xsl:element name="dc:type">
			<xsl:text>Calculation or Conversion Tool</xsl:text>
		</xsl:element>
	</xsl:if>

first find
<xsl:template match="d:itemRecord">
	 <nsdl_dc:nsdl_dc>

"""

__author__ = 'ostwald'

import re, sys, os
import requests
import lxml.etree as ET

default_namespaces = {
	'xsl' : "http://www.w3.org/1999/XSL/Transform",
	'dc' : "http://purl.org/dc/elements/1.1/",
	'nsdl_dc' : "http://ns.nsdl.org/nsdl_dc_v1.02/"
}

path = '/Users/ostwald/devel/DLS_Stack/dls-repository-stack/dcs-webapp/web/WEB-INF/xsl_files/adn-v0.6.50-to-nsdl_dc-v1.02-asn-identifiers.xsl'

tree = ET.parse(path)

def select(selector, base=tree, namespaces=default_namespaces):
	selected = base.xpath(selector, namespaces=namespaces)
	# if part isn't found, throw error
	if len(selected) != 1:
		raise Exception, "%d selected - expected 1" % len(selected)
	return selected[0]

def selectall (selector, base=tree, namespaces=default_namespaces):
	return base.xpath(selector, namespaces=namespaces)


# print ET.tostring(tree, pretty_print=1)

# nsdl_dc = select ('//nsdl_dc:nsdl_dc')

ifs = selectall ('//xsl:if')
print '%d ifs found' % len(ifs)

"""
now filter the ifs for these
<xsl:if test="contains($allresourceTypes, 'Calculation or conversion tool')">
"""

class Rule:

	def __init__(self, el):
		self.el = el
		self.name = self.el.get('name')
		self.text = ''
		self.type = ''

		for child in self.el:
			# 	print  ET.tostring (child, pretty_print=1)
			# print ' - %s' % child.tag
			if child.tag.endswith('text'):
				self.text = child.text
			if child.tag.endswith('attribute'):
				self.type = child.text


	def __repr__ (self):
		# return "%s (%s) - %d" % (self.text, self.type, len(self.el))
		if len(self.el) > 1:
			return "%s (%s)" % (self.text, self.type)
		else:
			return self.text

class RuleSet:

	def __init__(self, el):
		self.el = el
		self.rules = map(Rule, self.el)
		self.srcType = self.getSrcResourceType()


	def getSrcResourceType (self):
		test = self.el.get('test')
		# print 'test: ', test

		if not re.match('contains', test):
			return ''

		pat = "contains\(\$allresourceTypes, \'([^\']*)"
		m = re.match(pat, test)
		if m:
			# print 'MATCH- %s' % m.group(1)
			return m.group(1)


	def __repr__ (self):
		s = ''
		s += self.srcType
		# return ET.tostring(self.el, pretty_print=1)

		s = ' - %s (%d)' % (s, len(self.rules))
		return s

def accept (rule):
	pat = "contains\(\$allresourceTypes"

	try:
		return re.match(pat, rule.get('test'))
	except:
		print 'accept error: %s' % sys.exc_info()[1]
	return False

rules = filter(lambda x:accept(x), selectall ('//xsl:if'))
print '%d rules found' % len(rules)

for rule in rules:
	r = RuleSet(rule)
	print '\n -- %s' % r.srcType
	for rule in r.rules:
		print rule

print 'fooberry'