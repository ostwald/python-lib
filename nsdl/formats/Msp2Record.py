"""
Msp2Record
"""
import sys, os
from JloXml import MetaDataRecord, XmlUtils

class NcsItemRecord (MetaDataRecord):

	xpath_delimiter = '/'
	id_path = 'record/general/recordID'
	
	xpaths = {
		'id' : id_path,
		'url' : 'record/general/url'
	}
	
	def getUrl (self):
		return self.get('url')
		
	def setUrl (self, val):
		self.set('url', val)
		
	def getLicenseUrlNodes (self):
		"""
		get nodes at record/rights/license/url
		"""
		return self.selectNodes (self.dom, 'record/rights/license/url')
	
	def getLicenseUrlValues (self):
		"""
		get values at record/rights/license/url
		"""
		return map (lambda x:XmlUtils.getText(x), self.getLicenseUrlNodes())
		
	def getIsPartOfUrlNodes (self):
		"""
		get nodes at record/relations/isPartOf/url
		"""
		return self.selectNodes (self.dom, 'record/relations/isPartOf/url')
	
	def getIsPartOfUrlValues (self):
		"""
		get values at record/relations/isPartOf/url
		"""
		return map (lambda x:XmlUtils.getText(x), self.getIsPartOfUrlNodes())
		
class Msp2Record (MetaDataRecord):
		
	def getContributorElements (self, role=None):
		contribs = []
		elements = self.selectNodes (self.dom, 'record/lifecycle/contributor')
		for contrib in elements:
			roleVal = contrib.getAttribute('role')
			if role is None or roleVal == role:
				contribs.append (contrib)
		return contribs
		
	def getPublishers (self):
		"""
		returns the element values for all contributor elements having
		a type attribute of value 'Publisher'
		"""
		return map (lambda x:XmlUtils.getText(x), self.getContributorElements('Publisher'))
		
	def getRightsElements (self):
		return self.selectNodes(self.dom, 'record/lifecycle/rights')
		
	def getRightsValues (self):
		return map (lambda x:XmlUtils.getText(x), self.getRightsElements())
	
class MathPathRecord (Msp2Record):
	"""
	math_path is a derivative of ms2
	"""

	pass
