import os, sys
from JloXml import MetaDataRecord, XmlUtils

# class ContactInfo:
	# """
	# not sure this is ready to go or even used 5/1/11
	# """
	# def __init__  (self, element):
		# self.element = element
		# self.emailElement = XmlUtils.getChild ('email', self.element)
		# self.phoneElement = XmlUtils.getChild ('phone', self.element)
		# 
	# def getEmail (self):
		# return XmlUtils.getText (self.emailElement)
		# 
	# def setEmail (self, value):
		# if not self.emailElement:
			# self.emailElement = self.element.appendChild (XmlUtils.createElement ("email"))
		# XmlUtils.setText (self.emailElement, value)
		# 
	# def getPhone (self):
		# return XmlUtils.getText (self.phoneElement)
		# 
	# def setPhone (self, value):
		# if not self.phoneElement:
			# self.phoneElement = self.element.appendChild (XmlUtils.createElement ("phone"))
		# XmlUtils.setText (self.phoneElement, value)	


class Affiliation:
	
	def __init__ (self, element):
		self.element = element
		
	def getInstName (self):
		return XmlUtils.getChildText(self.element, 'instName')
		
	def setInstName (self, instName):
		"""
		Affiliations have ONE instName element
		if an instName element does not exist, create one
		set the text of the instName element to provided instName value
		"""
		instNameEl = XmlUtils.getChild ('instName', self.element)
		if not instNameEl:
			instNameEl = self.element.appendChild (XmlUtils.createElement('instName'))
			print 'created instNameEl: ' + instNameEl.toxml()
		XnlUtils.setText(instNameEl, instName)
		return instNameEl
		
	def getInstDiv (self, instDiv):
		"""
		looks for the provided instDiv VOCAB in this Afflilation
		"""
		instDivEls = XmlUtils.selectNodes (self.element, 'instDivision')
		## print "%d instDiv elements found" % len(instDivEls)
		for instDivEl in instDivEls:
			if XmlUtils.getText (instDivEl) == instDiv:
				return instDivEl
		
	def addInstDivVocab (self, instDivVocab):
		"""
		add all the segments of the provided instDivVocab (that
		do not already exist) to this Affliation.
		NOTE: we don't add the first split by itself, the first
		split we add is [0:1]
		"""
		splits = instDivVocab.split(":")
		for i in range (1, len(splits)):
			vocab = ':'.join(splits[:i+1])
			if not self.getInstDiv (vocab):
				instDiv = XmlUtils.createElement("instDivision")
				XmlUtils.setText (instDiv, vocab)
				self.element.appendChild (instDiv)
				# print "\nadded instDiv: %s" % vocab
		
	def sortInstDivs (self):
		instDivEls = XmlUtils.selectNodes (self.element, 'instDivision')
		instDivEls.sort(lambda x, y:cmp(XmlUtils.getText(x), XmlUtils.getText(y)))
		for node in instDivEls:
			self.element.appendChild(node)
		
class Contributor:
	
	def __init__ (self, element):
		self.element = element
		# self.affiliationElement = 
		self.role = element.getAttribute ("role")
		
	def getAffiliationElements (self):
		return XmlUtils.selectNodes (self.element, 'affiliation')
		
	def getAffiliation (self, instName):
		"""
		affilations are associated with ONE instName
		returns Affilation instance for provided instName, creating if necessary
		"""
		affiliationEl = None
		for node in self.getAffiliationElements():
			instNameEl = XmlUtils.getChild('instName', node)
			if XmlUtils.getText(instNameEl) == instName:
				affiliationEl = node
				break
		if not affiliationEl:
			affiliationEl = self.element.appendChild (XmlUtils.createElement('affiliation'))
			instNameEl = affiliationEl.appendChild (XmlUtils.createElement('instName'))
			XmlUtils.setText(instNameEl, instName)
		return Affiliation (affiliationEl)
		
	# def setInstName (self, instName):
		# self.getAffiliation().setInstName (instName)
		
	def getUcarAffiliation (self):
		"""
		returns an Affiliation instance for UCAR, creating if necessary
		"""
		return self.getAffiliation('University Corporation for Atmospheric Research (UCAR)')
		
	# def getAffiliation (self, instName):
		# """
		# gets the Affiliation for this Contributor that matches provided instName
		# returns None if such Affliation not found
		# """
		# for affEl in XmlUtils.getChildElements(self.element, 'affiliation'):
			# affiliation = Affiliation (affEl)
			# if affiliation.getInstName() == instName:
				# return affiliation
		

class ContributorPerson (Contributor):
	"""
	represent information found at the /record/contributors/person node
	- lastName
	- firstName
	- middleName
	- secondMiddleName
	- suffix
	- publishingName
	- order
	- upid
	"""
	# these are the simple elements (in schema-order) for Person
	simple_child_tags = ['lastName', 'firstName', 'middleName', 'secondMiddleName', 'suffix', 'publishingName']
	
	# these are ALL the elements (in schema-order) for person
	element_order = simple_child_tags + ['contactInfo', 'affiliation']
	
	def __init__ (self, element):
		Contributor.__init__ (self, element)
		for attr in self.simple_child_tags:
			setattr (self, attr, XmlUtils.getChildText (element, attr))
		try:
			self.order = int(element.getAttribute ("order"))
		except:
			self.order = ""
		self.upid = element.getAttribute ("UCARid")

	def updateElement (self):
		"""
		update the element in place with current values
		"""
		for attr in self.simple_child_tags:
			val = getattr(self, attr)
			if val:
				self.setChildElementValue(attr, val)
				
		if self.upid:
			self.element.setAttribute ("UCARid", self.upid)

	def setChildElementValue (self, tag, value):
		# print "TAG:%s, VALUE: %s" % (tag, value)
		child = XmlUtils.getChild (tag, self.element)
		if not child:
			child = self.element.appendChild(XmlUtils.createElement(tag))
		XmlUtils.setText (child, value)
		
	def __repr__ (self):
		## return "%d - %s, %s (%s)" % (self.order, self.lastName, self.firstName, self.role)
		return "%s, %s (%s)" % (self.lastName, self.firstName, self.role)
		
	def __cmp__ (self, other):
		return cmp (self.order, other.order)
		
	def setEmail (self, email):
		self.setContactInfoProp ('email', email)	
		
	def getEmail (self):
		return self.getContactInfoProp ('email')
		
	def setContactInfoProp (self, prop, val):
		contactInfoEl = XmlUtils.getChild ('contactInfo', self.element)
		if not contactInfoEl:
			contactInfoEl = self.element.appendChild (XmlUtils.createElement ('contactInfo'))
		contactInfoEl.setAttribute (prop, val)	
		
	def getContactInfoProp (self, prop):
		contactInfoEl = XmlUtils.getChild ('contactInfo', self.element)
		if not contactInfoEl:
			return None
		return contactInfoEl.getAttribute(prop)

	def orderElements(self):
		"""
		enforce schema-ordering of child elements
		"""
		elements = XmlUtils.getChildElements(self.element)
		keyFn = lambda x:self.element_order.index(x.tagName)
		elements.sort (key=keyFn)
		for el in elements:
			self.element.appendChild(el)

		
class ContributorOrganization (Contributor):
	"""
	represent information found at the /record/contributors/person node
	"""
	
	def __init__ (self, element):
		Contributor.__init__ (self, element)	
		
	def __repr__ (self):
		return "%d - %s, %s (%s)" % (self.order, self.lastName, self.firstName, self.role)
		
class OsmRecord (MetaDataRecord):

	xpath_delimiter = '/'
	id_prefix = "OSM-RECORD"
	
	nameSpaceUri="http://nldr.library.ucar.edu/metadata/osm" 
	schemaUri="http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/osm.xsd"
  
	id_path = 'record/general/recordID'
	
	xpaths = {
		'id' : 'record/general/recordID',
		'recordDate' : 'record/general/recordDate',
		'title' : 'record/general/title',
		'pubName' : 'record/general/pubName',
		'lastName' : 'record/contributors/person/lastName',
		'firstName' : 'record/contributors/person/firstName',
		'middleName' : 'record/contributors/person/middleName',
		'suffix' : 'record/contributors/person/suffix',
		# 'fiscalYear': 'record/coverage/fiscalYear',  #no longer in schema - use /record/coverage/date[@type='???']
		'coverageDate' : 'record/coverage/date',
		'volume' : 'record/general/volume',
		'issue' : 'record/general/issue',
		'pages' : 'record/general/pages',
		'pageSpan' : 'record/general/pageSpan',
		'abstract' : 'record/general/abstract',
		'pub_id' : 'record/classify/idNumber',
		'classification' : 'record/classify/classification',
		'status' : 'record/classify/status',
		'copyrightNotice' : 'record/rights/copyrightNotice'
	}
	
	# defined by schema but unfortunately hard-coded here
	root_child_order = [
		'general',
		'resources',
		'contributors',
		'classify',
		'coverage',
		'rights'
	]
	
	general_child_order = [ 
		'recordID',
		'recordDate',
		'urlOfRecord',
		'pubName',
		'seriesTitle',
		'eventName',
		'volume',
		'issue',
		'edition',
		'appVersion',
		'pageSpan',
		'pageTotal',
		'pages',
		'title',
		'altTitle',
		'earlierTitle',
		'laterTitle',
		'description',
		'abstract',
		'keyword',
		'OSMsubject',
		'LCSHsubject',
		'thumbnail'
	   ]
	
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path=path, xml=xml)
		self.dateMap = None
		
	def getId(self):
		# return self.getTextAtPath (self.id_path)
		return self.get ('id')
		
	def setId(self, id):
		# self.setTextAtPath (self.id_path, id)
		self.set ('id', id)
		
	def getRecordDate (self):
		"""
		gets value of /record/general/recordDate
		"""
		return self.get ('recordDate')
		
	def getTitle (self):
		return self.get ('title')
		
	# def getFiscalYear (self):
		# return self.get('fiscalYear')
		# 
	# def setFiscalYear (self, fiscalYear):
		# self.set('fiscalYear', fiscalYear)
		
	def getPubName (self):
		return self.get('pubName')
		
	def getVolume (self):
		return self.get('volume')
		
	def getIssue (self):
		return self.get('issue')
		
	def setPubName (self, pubName, pubNameType=None):
		"""
		creates pubName element if one doesn't exist
		ASSUMES A TITLE ELEMENT EXISTS for proper insertion
			(inserts following title element)
		"""
		if not self.selectSingleNode (self.dom, self.xpaths['pubName']):
			# create pubNamem element now, but we populate later
			pubNameEl = XmlUtils.createElement("pubName")
			
			## now find where to insert pubNameEl
			generalEl = self.selectSingleNode (self.dom, 'record/general')
			if not generalEl:
				raise Exception, "record does not contain a general element"
			gen_children = XmlUtils.getChildElements(generalEl)
			print "%d elements found" % len(gen_children)
			targetEl = None
			for child in gen_children:
				print ' - ', child.tagName
				if not child.tagName in ['recordID', 'recordDate', 'urlOfRecord']:
					targetEl = child
					print "target is %s" % child.tagName
					break
					
			if targetEl:
				# insert after targetEl
				generalEl.insertBefore (pubNameEl, targetEl)
			else:
				# insert at end of general element
				XmlUtils.addElement (self.dom, generalEl, 'pubName')
			
		self.set ('pubName', pubName)
		if pubNameType:
			self.setPubNameType (pubNameType)
			
	def setPubNameType (self, pubNameType):
		el = self.selectSingleNode (self.dom, self.xpaths['pubName'])
		if not el:
			raise Exception, "setPubType could not find pubName element"
		el.setAttribute ("type", pubNameType)
	
	def getPubNameType (self):
		el = self.selectSingleNode (self.dom, self.xpaths['pubName'])
		return el and el.getAttribute ("type") or None
		
	def getAuthors (self):
		"""
		returns a list of author elements
		"""
		authors = []
		people = self.selectNodes (self.dom, "record/contributors/person")
		for person in people:
			if person.getAttribute("role") == "Author":
				authors.append (person)
		return authors
		
	def setTitleType (self, titleType):
		el = self.selectSingleNode (self.dom, self.xpaths['title'])
		if not el:
			raise Exception, "setTitleType could not find title element"
		el.setAttribute ("type", titleType)
		
	def getTitleType (self):
		"""
		same as ResourceType
		"""
		titleNode = self.selectSingleNode (self.dom, self._xpath('title'))
		if titleNode:
			return titleNode.getAttribute ("type")
		
	def setTitle (self, title, titleType=None):
		self.set ("title", title)
		if titleType:
			self.setTitleType(titleType)
		
	def deleteElementsAtPath (self, xpath):
		"""
		removes all elements at specified xpath
			for example, to remove record/rights/access field
		"""
		elements = self.selectNodes (self.dom, xpath)
		if elements:
			print '%d elements found at %s' % (len(elements), xpath)
			for el in elements:
				self.deleteElement (el)
			self.write()
			print "updated %s" % self.getId()
		
	def getContributorPeople (self, role=None):
		"""
		gets list of ContributorPerson instances
		"""
		contributorPeople = []
		people = self.selectNodes (self.dom, "record/contributors/person")
		for personNode in people:
			if (not role) or personNode.getAttribute ('role') == role:
				contributorPeople.append (ContributorPerson (personNode))

		contributorPeople.sort()			
		return contributorPeople
		
	def getContributorOrgs (self, role=None):
		contributorOrgs = []
		orgs = self.selectNodes (self.dom, "record/contributors/organization")
		for orgNode in orgs:
			if (not role) or orgNode.getAttribute ('role') == role:
				contributorOrgs.append (ContributorOrganization (orgNode))			
		return contributorOrgs
			
	def getPubDate (self):
		"""
		/record/coverage/date[@type='Published'
		"""
		return self.getTypedDate ('Published')
				
	def getTypedDate (self, dateType):
		for date in self.getDateNodes():
			if date.getAttribute ("type") == dateType:
				return XmlUtils.getText (date)		
				
	def getDateNodes (self):
		return self.selectNodes (self.dom, self._xpath("coverageDate"))
		
	def getDate (self, dateType=None):
		dateMap = self.getDateMap()
		if dateType is not None:
			return dateMap.has_key(dateType) and dateMap[dateType]
		else:
			return len(foo) == 0 and None or dateMap.values()[0]
		
	def setDate (self, dateStr, dateType):
		coverageNode = self.selectSingleNode (self.dom, 'record/coverage')
		if not coverageNode:
			#raise Exception, "no coverage node found"
			coverageNode = XmlUtils.addElement(self.dom, self.doc, "coverage")
		targetDateElement = None
		dateNodes = self.getDateNodes()
		if dateNodes:
			for node in dateNodes:
				if node.hasAttribute (dateType):
					targetDateElement = node
		if targetDateElement is None:
			targetDateElement = XmlUtils.createElement ("date")
			targetDateElement.setAttribute ("type", dateType)
			coverageChildren = XmlUtils.getChildElements (coverageNode)
			if coverageChildren:
				firstChild = coverageChildren[0]
				coverageNode.insertBefore (targetDateElement, firstChild)
			else:
				coverageNode.appendChild (targetDateElement)
		XmlUtils.setText (targetDateElement, dateStr)
		return targetDateElement
				
	def getPubsId (self):
		"""
		pubId assgined to this publication in NESL PUBS database
		should be present in some osgc (before a certain date) and all of pubs-ref, and 'pub
		/record/classify/idNumber
		type='PUBID'
		"""
		nodes = self.selectNodes(self.dom, 'record/classify/idNumber')
		# if nodes is None: return None
		for node in nodes:
			pubsId = node.getAttribute('type') 
			if pubsId == 'PUBID':
				return XmlUtils.getText(node)
		
	def getDateMap (self):
		"""
		create a map of dateType -> dateValue
		"""
		if self.dateMap is None:
			self.dateMap = {}
			for dateNode in self.getDateNodes():
				dateType = dateNode.getAttribute ("type")
				dateValue = XmlUtils.getText (dateNode)
				if self.dateMap.has_key (dateType):
					existingValue = self.dateMap[dateType]
					if type(existingValue) != type([]):
						existingValue = [existingValue]
					existingValue.append (dateValue)
					self.dateMap[dateType] = existingValue
				else:
					self.dateMap[dateType] = dateValue
		return self.dateMap
			
	def getPublishedUrl (self):
		"""
		fetches first relation url with type="Is published" 
		<relation type="Is published" url="some url"/>
		"""
		relations = self.selectNodes (self.dom, 'record/resources/relation')
		for relation in relations:
			if relation.getAttribute ("type") == "Is published" and \
			   relation.hasAttribute("url"):
					
				   return relation.getAttribute("url")
				   
	def getDoi (self):
		"""
		doi's are catalged as /records/classify/idNumber, with type="DOI"
		"""
		idNumbers = self.selectNodes (self.dom, 'record/classify/idNumber')
		for id in idNumbers:
			if id.getAttribute ("type") == "DOI":
				return XmlUtils.getText(id)
		
	def getCopyrightNotice (self):
		return self.get ('copyrightNotice')
		
	def setCopyrightNotice (self, val):
		self.set ('copyrightNotice', val)
		
	def getStatus(self):
		return self.get ('status')
		
	def getPageSpan(self):
		return self.get ('pageSpan')
		
	def getFundingEntityNodes (self):
		return self.selectNodes ('record/classify/fundingEntity')
		
	def getRootChild (self, childName):
		if not childName in self.root_child_order:
			raise Exeption, 'Unrecognized childName: "%s"' % childName
		child = self.selectSingleNode(self.dom, 'record/'+childName)
		if not child:
			child = XmlUtils.addElement(self.dom, self.doc, childName)
			XmlUtils.orderElements(self.doc, self.root_child_order)
			
		return child
		
	def addGeneralChild (self, childName):
		"""
		add a named child element to the /record/general node
		"""
		if not childName in self.general_child_order:
			raise Exeption, 'Unrecognized childName: "%s"' % childName
		general = self.getRootChild('general')
		child = XmlUtils.addElement(self.dom, general, childName)
		XmlUtils.orderElements(general, self.general_child_order)
			
		return child
		
if __name__ == '__main__':
	#path = 'C:/Documents and Settings/ostwald/devel/dcs-instance-data/local-ndr/records/osm/soars/SOARS-000-000-000-100.xml'
	path = 'test-osm-instance.xml'
	rec = OsmRecord (path=path)

	print rec.getRecordDate()
	if 0:
		for contrib in rec.getContributorPeople("Submitter"):
			print contrib
	elif 0:
		print "PublishedUrl:", rec.getPublishedUrl()
	else:
		print "doi:", rec.getDoi()
