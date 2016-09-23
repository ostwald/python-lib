"""
submit a query to solr and display results

write util to display all fields (fields are children of response/result/doc)

add fl param to limit fields returned
"""

import os,sys,re,time
from UserList import UserList
from UserDict import UserDict
import requests
from lxml import etree

field_spec = [
	['title', 'mods_titleInfo_title_ms'],
	['doi', 'mods_identifier_doi_ms'],
	['ark', 'mods_identifier_ark_s'],
	['date', 'keyDateYMD'],
	['description', 'mods_abstract_s'],
	['publisher', 'mods_originInfo_publisher_s'],
	['genre', 'mods_genre_s'],
	['collection', 'mods_extension_collectionKey_ms'],
	['creator', 'Display_Name_with_Full_Affiliation'],
	['classification', 'mods_extension_classification_mt'],
	['useAndReproduction', 'mods_accessCondition_use_and_reproduction_s'],
	['nldrCitableUrl', 'mods_identifier_type_uri_displayLabel_Legacy_citable_URL'],
]

class FieldHelper:
	
	def __init__ (self):
		self.solrFieldMap = {}
		for spec in field_spec:
			self.solrFieldMap[spec[1]] = spec[0]
	
	def getSolrFieldList (self):
		return map (lambda x: x[1], field_spec)
		
	def getResponseField (self, solrField):
		return self.solrFieldMap[solrField]

class SolrResponseDoc (UserList):
	"""
	implements List API - items are SolrResult instances
	
	root is the solr response root element
	"""
	dec_pat = re.compile("<\?xml version=\"1.0\"( encoding=\"UTF-8\")\?>")
	
	def __init__ (self, xml):
		self.data = []
		
		m = self.dec_pat.match(xml)
		if m:
			#etree does not like the XML declaration
			# xml = self.dec_pat.sub('', xml, 1)
			xml = xml.replace(m.group(1),'', 1) # maybe more effecient?
		
		self.root = etree.fromstring(xml)
		self.data = map (SolrResult, self.root.xpath('/response/result/doc'))
		
class SolrResult (UserDict):
	"""
	One "hit" returned by solr search
	
	root is "doc" element and all children are fields
	
	"""
	def __init__ (self, root):
		self.data = {}
		self.fieldHelper = FieldHelper()
		self.root = root
		self._initFieldValueMap()

		
	def __repr__ (self):
		return etree.tostring(self.root, pretty_print=True)
		
	def getUniqueModsFields (self):
		return sorted (filter (lambda x:x.startswith("mods_"), self.getFields()))

	def getFields (self):
		# for all children of root, get the name attribute
		return map (lambda x:x.get('name'), self.root)
		
	def getFieldValue(self, field):
		return self[field]
		
	def getMods (self):
		parent = self.root.xpath("//arr[@name='ds.MODS']")[0]
		# print "%d MODS" % len(parent)
		if parent is not None:
			return parent[0].text.strip()
			# return etree.tostring(parent[0], pretty_print=True, method="xml")
			# return etree.dump(parent[0])

	def transform (self):
		"""
		create the service response representation of this SolrResult
		we replace solr field names with response field names (see FieldHelper)
		"""
		t_root = etree.XML("<result/>")
		for field_name in self.keys():
			value = self[field_name]
			response_tag = None
			try:
				response_tag = self.fieldHelper.getResponseField(field_name)
			except KeyError, msg:
				print "skipping field: %s" % field_name
				continue
				
			# tag = type(value) == type([]) and 'arr' or 'str'
			if type(value) == type(''):
				newchild = etree.SubElement(t_root, response_tag)
				newchild.text = value
			else:
				# value is a list
				for item in value: 
					newchild = etree.SubElement(t_root, response_tag)
					newchild.text = item
				
		return t_root

	def _initFieldValueMap (self):
		for child in self.root:
			name = child.get('name')
			value = None
			tag = child.tag
			if tag == 'str':
				value = child.text
			elif tag == 'arr':
				value = []
				for gchild in child:
					value.append(gchild.text)
			self[name] = value


class SolrRequest:

	# submit a request
	baseUrl = "http://osstage2.ucar.edu:8080/solr/core1/select"
	
	default_params = {
		# 'fl':'fgs_label_s' # 
		'wt': 'xml',
		'indent':'true'
	}
	
	result_constructor = SolrResponseDoc

	def __init__ (self, params={}):
		self.fieldHelper = FieldHelper()
		self.default_params['fl'] = ','.join(self.fieldHelper.getSolrFieldList())
		
		# get full Mods record
		self.default_params['fl'] = self.default_params['fl'] + " " + 'ds.MODS'
		
		print "DEFAULT FIELD LIST: " + self.default_params['fl']
		
		self.params = params;
		self.params.update (self.default_params)
		self.responseDoc = self.get()
	
	def showParams(self):
		for key in self.params.keys():
			print ' - %s: %s' % (key, self.params[key])
	
	def get (self):
		try:
			r = requests.get (self.baseUrl, params=self.params)
		except Exception, msg:
			print "request Error: %s", msg
			
		try:
			return self.result_constructor (r.text)
		except Exception, msg:
			print 'SolrResponseDoc ERROR: %s' % msg

def requestTester ():
	params = {
		# 'q' : 'mods_extension_collectionKey_ms:technotes',
		'q' : 'Creator_Lastname:"ostwald"',
		'rows' : '1',
		'wt': 'xml',
		'indent': 'true'
	}
	request = SolrRequest(params)
	print "\nrequest params"
	request.showParams()
	doc = request.responseDoc
	# print 'MODS: %s' % doc[0].getMods()
	print '%d results in resultDoc' % len(doc)
	
	print 'TRANSFORMED'
	print etree.tostring(doc[0].transform(), pretty_print=True)
	
	if 0:
		result = doc[0]
		# fields = result.getFields()
		fields = result.getUniqueModsFields()
		print "%d mods fields" % len (fields)
		for f in fields: print ' -%s' % f

def staticDocTester():
	path = '/Library/WebServer/Documents/solr/solr.xml'
	# path = 'tiny.xml'
	content = open(path,'r').read()
	doc = SolrResponseDoc(content)
	print doc
	# doc.getFields()
	#doc.getUniqueModsFields()
	
def fieldHelperTester():
	helper = FieldHelper()
	solr_fields = helper.getSolrFieldList()
	for f in solr_fields:
		print ' - %s' % f
		
def resultDocTester ():
	params = {
		'q' : 'mods_extension_collectionKey_ms:technotes',
		'q' : 'Creator_Lastname:"ostwald"',
		'rows' : '1',
		'wt': 'xml',
		'indent': 'true'
	}
	result = SolrRequest(params).responseDoc[0]
	fields = result.getUniqueModsFields()
	print "%d mods fields" % len (fields)
	print 'SOLR'
	print result
	print 'TRANSFORMED'
	print etree.tostring(result.transform(), pretty_print=True)

if __name__ == '__main__':
	requestTester ()
	# staticDocTester()
	# fieldHelperTester()
	# resultDocTester()
	

