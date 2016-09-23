from prov_item_cmp import ProvItemCompareHelper, getPubsItemsMgr, DataHubItemsMgr
# from state_countries_xsd import getPubsItemsMgr
from JloXml import XmlRecord, XmlUtils

class OPML:
	
	"""
	make the body element and then attach
	- outline for country type="group" text="countryName"  ?? does this element get a vocab attribute? 
		- outlines for provs (type="vocab" text="${provName}" vocab="${provCode})
	"""
	
	xsd_path = "xsd/state-countries.xsd"
	
	def __init__ (self):
		self.xsdMgr = getPubsItemsMgr (self.xsd_path)
	
	def getCountriesType (self):
		# xsd_path = "merged/merged-state-countries.xsd"
		countriesType = self.xsdMgr.xsd.getCountriesType()
		# print "countriesType contains %d terms" % len(countriesType)
		return countriesType

	def countryTermSortFn (self, c1, c2):
		if c1.countryName == "United States of America": return -1
		if c2.countryName == "United States of America": return 1
		return cmp (c1.countryName,c2.countryName)
		
	def makeCountriesOutline (self):
		# keys = self.xsdMgr.countryCodes.keys()
		# keys.sort (self.countryTermSortFn)

			
		rec = XmlRecord(xml="<body/>")
		body = rec.doc
		countriesOutline = XmlUtils.addElement(rec.dom, body, "outline")
		countriesOutline.setAttribute ("type", "group")
		countriesOutline.setAttribute ("text", "Countries")
		
		countryCodes = self.xsdMgr.countryCodes.values()
		countryCodes.sort (self.countryTermSortFn)
		for countryTerm in countryCodes:

				countryOutline = XmlUtils.addElement(rec.dom, countriesOutline, "outline")
				countryOutline.setAttribute ("type", "vocab")
				countryOutline.setAttribute ("text", countryTerm.countryName)
				countryOutline.setAttribute ("vocab", countryTerm.countryCode) # don't think we want to do this

		return rec

	def provTypeSortFn (self, provTypeName1, provTypeName2):
		if provTypeName1 == "usType": return -1
		if provTypeName2 == "usType": return 1
		return cmp(provTypeName1, provTypeName2)
		
	def makeProvsOutline (self):
		rec = XmlRecord(xml="<body/>")
		body = rec.doc
		typeDefs = self.xsdMgr.provTypes
		# typeDefs.sort (self.provTypeSortFn)
		
		provTypeNames = typeDefs.keys()
		provTypeNames.sort (self.provTypeSortFn)
		for provTypeName in provTypeNames:
			
			# print provTypeName
			# continue
			
			provItems = typeDefs[provTypeName].values();
			provItems.sort()
			item = provItems[0] # all provItems share the same country information
			
			# print "**", typeDef.__class__.__name__
			countryOutline = XmlUtils.addElement(rec.dom, body, "outline")
			countryOutline.setAttribute ("type", "group")
			countryOutline.setAttribute ("text", item.countryName)
			#countryOutline.setAttribute ("vocab", item.countryCode) # don't think we want to do this
				
			for provTerm in provItems:
				provOutline = XmlUtils.addElement(rec.dom, countryOutline, "outline")
				provOutline.setAttribute ("type", "vocab")
				provOutline.setAttribute ("text", provTerm.provName)
				provOutline.setAttribute ("vocab", provTerm.provCode) # don't think we want to do this

		return rec
		
	def makeProvsOutlineOLD (self):
		rec = XmlRecord(xml="<body/>")
		body = rec.doc
		typeDefs = self.xsdMgr.xsd.getProvTypes()
		# typeDefs.sort (self.provTypeSortFn)
		for typeDef in typeDefs:
			
			print typeDef.countryName
			continue
			
			provItems = typeDef.getValues();
			item = provItems[0] # all provItems share the same country information
			
			# print "**", typeDef.__class__.__name__
			countryOutline = XmlUtils.addElement(rec.dom, body, "outline")
			countryOutline.setAttribute ("type", "group")
			countryOutline.setAttribute ("text", item.countryName)
			#countryOutline.setAttribute ("vocab", item.countryCode) # don't think we want to do this
				
			for provTerm in provItems:
				provOutline = XmlUtils.addElement(rec.dom, countryOutline, "outline")
				provOutline.setAttribute ("type", "vocab")
				provOutline.setAttribute ("text", provTerm.provName)
				provOutline.setAttribute ("vocab", provTerm.provCode) # don't think we want to do this

		return rec
		
	# def makeCountriesOutline (self):
		# typeDef = self.xsdMgr.xsd.getCountriesType()
		# return self.makeOutline ([typeDef])
				
if __name__ == '__main__':
	opml = OPML()
	print opml.makeProvsOutline()
	# print opml.makeCountriesOutline()
