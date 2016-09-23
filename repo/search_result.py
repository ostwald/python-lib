"""
SearchResult - encapsulates a search result from the DDS search service
"""
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils

class StoredContent (UserDict):
	"""
	storedContent reports named, indexed fields, which appear in the response as follows:
	
	<storedContent>
	  <content fieldName="dcsstatus">_|-final-osgc-|_</content>
	</storedContent>
	"""
	def __init__ (self, element):
		UserDict.__init__ (self)
		if element is None:
			return
		for node in XmlUtils.getChildElements (element, "content"):
			field = node.getAttribute ("fieldName")
			value = XmlUtils.getText (node)
			if self.has_key (field):
				curVal = self[field]
				if type(curVal) != type([]):
					curVal = [curVal, value]
				else:
					curVal.append (value)
				self[field] = curValue
			else:
				self[field] = value
				
	def get (self, field):
		if not self.has_key(field):
			return None
		return self[field]
		
	def keys (self):
		sorted = self.data.keys()
		return sorted
		
	def report (self):
		for key in self.keys():
			print "%s: %s" % (key, self[key])
				
class SearchResult(XmlRecord):
	"""
	exposes:
		- recId
		- xmlFormat
		- fileLastModified
		- collection, collectionName
		- storedContent - (StoredContent instance)
		- dcsstatus, dcsstatusNote, dcsisValid
		- payload (an XmlRecord instance)
		
	overwrite default_payload_constructor to specify a class to use
	to instantiate the payload (default is XmlRecord).
	"""
	default_payload_constructor = XmlRecord
	
	def __init__ (self, element, payload_constructor=None):
		self.payload_constructor = payload_constructor or self.default_payload_constructor
		XmlRecord.__init__ (self, xml=element.toxml())
		# self.recId = self.getTextAtPath("head:id")
		self.recId = self.getTextAtPath("record:head:id")
		self.xmlFormat = self.getTextAtPath("record:head:xmlFormat")
		self.fileLastModified = self.getTextAtPath ("record:head:fileLastModified")
		self.collection = self.get_collection()
		self.collectionName = self.get_collectionName()
		self.storedContent = StoredContent (self.selectSingleNode (self.dom, "record:storedContent"))
		self.dcsstatus = self.get_status()
		self.dcsstatusNote = self.storedContent.get('dcsstatusNote')
		self.dcsisValid = self.storedContent.get('dcsisValid')
		self.payload = self.get_payload ()
		
	def get_payload (self):
		metadata = self.selectSingleNode (self.dom, "record:metadata")
		children = XmlUtils.getChildElements(metadata)
		if not children:
			raise Exception, "Could not find payload"
		if len(children) != 1:
			raise Exception, "Found multiple payload elements"
		return self.payload_constructor (xml=children[0].toxml())
		
	def get_collection (self):
		node = self.selectSingleNode (self.dom, "record:head:collection")
		if node:
			return node.getAttribute("key")
			
	def get_collectionName (self):
		node = self.selectSingleNode (self.dom, "record:head:collection")
		if node:
			return XmlUtils.getText(node)

	def get_status (self):
		status = self.storedContent.get("dcsstatus")
		if status and status.find("_|-") == 0:
			status = "Final"
		return status
			
	def report(self):
		print self.recId, self.collection, self.dcsstatus
		# self.storedContent.report()
		# print self.payload
		

