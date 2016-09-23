"""
http://localhost:8080/schemedit/services/ddsws1-1?field=$facets&verb=ListTerms

"""
import os, sys, re
from serviceclient import SimpleClient
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, getAssetPath
from url_rewriting_records import urlRewritingRecordClasses

baseUrl = 'http://dls-pyramid.dls.ucar.edu:8080/schemedit/services/ddsws1-1' # BSCS Merge DCS

host = os.environ['HOST']
# print 'host:', host

if host == 'purg.local':
	baseUrl = 'http://localhost:8070/curricula/services/ddsws1-1' # BSCS Merge DCS

def getResponseDoc (params):
	postData = {}
	client = SimpleClient (baseUrl)
	# data = client.getData(params=params)
	# print data
	responseDoc = client.getResponseDoc (params)
	
	#here of course we could validate
	
	return responseDoc

def getFacetTerms ():
	params = {
		"field":"$facets",
		"verb": "ListTerms",
		}
			
	responseDoc = getResponseDoc (params)
	# print responseDoc
	term_nodes = responseDoc.selectNodes(responseDoc.dom, "DDSWebService:ListTerms:terms:term")
	return map (lambda x:XmlUtils.getText(x), term_nodes)
		


if __name__ == '__main__':
	
	assetCollections = ['comment_bscs', 'pbis-tips']
	assetXmlFormats = ['adn', 'dlese_anno', 'nsdl_dc', 'assessments']
	
	query = "url:h*ccs.dls.ucar.edu/protected/*"  # will this even work?
	
	if 0:
		query += ' AND ( %s )' % ' OR '.join(assetCollections)
	
		print 'query: ' + query;
	
		params = {
		"field":"$facets",
		"verb": "ListTerms",
		}
	

	terms = getFacetTerms()
	print "%d terms found" % len(terms)


