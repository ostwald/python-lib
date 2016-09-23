"""
OsmRecordUpdater

Extends OsmRecord. This class is responsible for performing updates on an osmRecord

- updateFiscalYear 
- updateRights

"""
import sys, os
from ncar_lib.osm import OsmRecord
from ncar_lib.repository.fiscal_year import getFiscalYearString
from JloXml import XmlUtils

class OsmRecordUpdater (OsmRecord):
	"""
	the root element (i.e., 'record') is an xs:all, meaning that we don't have to worry about node order.
	therefore, we can always append children e.g., coverage, rights to the root. 
	"""
	
	removeFiscalDates = 1
	
	def getCoverageNode (self):
		coverageNode = self.selectSingleNode (self.dom, 'record/coverage')
		if not coverageNode:
			coverageNode = XmlUtils.addElement(self.dom, self.doc, "coverage")
		return coverageNode
		
	def getRightsNode (self):
		rightsNode = self.selectSingleNode (self.dom, 'record/rights')
		if not rightsNode:
			rightsNode = XmlUtils.addElement(self.dom, self.doc, "rights")
		return rightsNode
		
	def getCopyrightNoticeNode (self):
		return self.selectSingleNode (self.dom, 'record/rights/copyrightNotice')

	def updateRights (self):
		
		copyrightNoticeNode = self.getCopyrightNoticeNode()
		if not copyrightNoticeNode:
			rightsNode = self.getRightsNode()
			copyrightNoticeNode =  self.getUnknownCopyrightNoticeElement()
			# print copyrightNoticeNode.toxml()
			XmlUtils.insertAsFirstChild(rightsNode, copyrightNoticeNode)
			print rightsNode.toxml()
		else:
			print "not updating, copyright present"
			
	def getUnknownCopyrightNoticeElement (self):
		"""<copyrightNotice type="Unknown" holder="Unknown" url="http://www.ucar.edu/legal/terms_of_use.shtml">
				Copyright information is unknown. Please contact the creator, author or publisher for further information.
			</copyrightNotice>
		"""

		el = XmlUtils.createElement ("copyrightNotice")
		XmlUtils.setText (el, "Copyright information is unknown. Please contact the creator, author or publisher for further information.")
		el.setAttribute ('type', 'Unknown')
		el.setAttribute ('holder', 'Unknown')
		el.setAttribute ('url', 'http://www.ucar.edu/legal/terms_of_use.shtml')
		return el
		
	def updateFiscalYear (self):
		"""
		"""
		fiscalYear = self.getFiscalYear()
		# print "fiscalYear: %s" % fiscalYear
		if fiscalYear:
			# no need to do anything
			return
			
		fiscalYear = None
		publishedDate = self.getTypedDate('Published')
		# print "publishedDate: %s" % publishedDate
		if publishedDate:
				fiscalYear = getFiscalYearString (publishedDate)
		else:
			createdDate = self.getTypedDate('Created')
			# print "createdDate: %s" % createdDate
			if createdDate:
				try:
					fiscalYear = getFiscalYearString (createdDate)
				except:
					print "WARNING: createdDate value (%s) for %s could not be parsed as date" %(createdDate, self.getId())
		
		# now fiscalYear insert in the dom. create an empty element if we don't have a value
		if fiscalYear is None:
			fiscalYear = ''

		self.insertFiscalYear(str(fiscalYear))
			
		if self.removeFiscalDates:
			self.removeFiscalDateNodes()

	def insertFiscalYear (self, fiscalYear):
		"""
		insert proviced fiscalYear in the dom
		
		if setFiscalYear fails the first call,
		the instance record does not have the necessary elements, which are created
		"""
		try:
			self.setFiscalYear (fiscalYear)
			return
		except:
			pass
		
		fyEl = XmlUtils.createElement('fiscalYear')
		coverageNode = self.getCoverageNode()
		# coverageNode = self.selectSingleNode (self.dom, 'record/coverage')
		if not coverageNode:
			raise Exception, "not not found at 'record/coverage' for %s" % self.getId()
		children = XmlUtils.getChildElements (coverageNode);
		if children:
			coverageNode.insertBefore(fyEl, children[0])
		else:
			coverageNode.appendChild(fyEl)
		self.setFiscalYear(fiscalYear)
		
	def removeFiscalDateNodes (self):
		"""
		remove any /record/coverage/date/@type="Fiscal" elements
		"""
		for dateNode in self.getDateNodes():
			if dateNode.getAttribute ("type") == 'Fiscal':
				self.deleteElement(dateNode)
		
class ArchiveRecordUpdater (OsmRecordUpdater):
	"""
	perform updates in ways specific to Archive and Oral history records
	"""
	def updateFiscalYear (self):
		"""
		set FiscalDate to 'N/A'
		"""
		self.insertFiscalYear ('N/A')
		if self.removeFiscalDates:
			self.removeFiscalDateNodes()
			
# setDate (self, dateStr, dateType):
	
def fyTester ():
	path = 'records/osm/gate/GATE-000-000-000-001.xml'
	
	if 0:
		updater = ArchiveRecordUpdater(path=path)
	else:
		updater = OsmRecordUpdater(path=path)
	
	updater.updateFiscalYear()
	print updater.getCoverageNode().toxml()
	print "fiscalYear: %s" % updater.getFiscalYear ()
	
if __name__ == '__main__':
	path = 'records/osm/gate/GATE-000-000-000-001.xml'
	
	if 0:
		updater = ArchiveRecordUpdater(path=path)
	else:
		updater = OsmRecordUpdater(path=path)
	
	updater.updateFiscalYear()
	# updater.updateRights()
	# print updater.getRightsNode().toxml()
	# print updater.getCoverageNode().toxml()
	print updater
