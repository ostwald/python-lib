"""
finds metadata records that catalog an asset with given filename

pattern :h*/protected/*/filename

needs to work over following collections:
- assessments
- ncs_item
- adn
- dlese_anno
- comm_anno

xmlFormats = ['adn', 'nsdl_dc', 'dlese_anno', 'comm_anno']

"""
import os, sys, re
# from repo import RepositorySearcher
from serviceclient import SimpleClient
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, getAssetPath
from url_rewriting_records import urlRewritingRecordClasses

class AssetSearcher (SimpleClient):
	
	def getFullUrl(self, params):
		return self.getRequest(params).get_full_url()
		
	def getSearchResults(self):
		pass

if __name__ == '__main__':
	fullurl = 'http://ccs.dls.ucar.edu/home/protected/assess_dps/dps_u1introHelicopter.pdf'
	# filename = 'dps_u1introHelicopter.pdf'
	filename = '*'
	# filename = 'svunit0act3_assess.pdf'
	
	baseUrl = "http://localhost:8070/curricula/services/ddsws1-1"
	params = {
		'verb' : "Search",
		'xmlFormat': 'dlese_anno',
		 # 'url' : 'http://ccs.dls.ucar.edu/home/protected/*/%s' % filename,
		 'n' : '10',
		 's' : '0',
		 'q' : ''
		# 'url' : fullurl
	}
	postData = {}
	client = AssetSearcher (baseUrl)
	# data = client.getData(params, postData)
	data = client.getResponseDoc(params, postData)	
	print data
	
	print client.getFullUrl(params)
