"""

"""
import os, sys
from JloXml import XmlRecord, XmlUtils

host = os.getenv("HOST")
# print host
if host == "taos.local":
	docBase = "/Documents/Work/DLS/NCAR Lib"
	develBase = "/Users/ostwald/devel/python-lib/ncar_lib"
elif host == "acorn" or host == "oak":
	docBase = "/home/ostwald/Documents/NCAR Library"
	develBase = '/home/ostwald/python-lib/ncar_lib'
elif host is None or host == "dls-sanluis":
	docBase = "H:/Documents/NCAR Library"
	develBase = 'H:/python-lib/ncar_lib'
else:
	# raise Exception, "Unknown host: %s" % host
	print 'WARNING host not recognized (%s)' % host

idListDir = os.path.join (develBase, "massage/idLists")

metadata = os.path.join (docBase, "metadata")
pdf = os.path.join (docBase, "pdf")
mappingDataPath = os.path.join (develBase, 'lib/accessionNumMappings.txt')

instMaps = os.path.join (docBase, "InstNameDiv-mapping")

collectionNameMap = {
	"theses" : "Cooperative Theses",
	"monographs" : "Monographs",
	"manuscripts" : "NCAR Manuscripts",
	"technotes" : "NCAR Technical Notes",
	"translations" : "NCAR Translations"
}
	
prefixMap = {
	"THESES": 'theses',
	'MONOGRAPH': 'monographs', 	
	'MANUSCRIPT': 'manuscripts', 
	'TECH-NOTE': 'technotes', 
	'TRANSLATION': 'translations'
	}

# see http://www.dlsciences.org/frameworks/library_dc/1.0/schemas/vocabs/instName.xsd
instNameType_vocab = [
	"National Center for Atmospheric Research (NCAR)",
	"University Corporation for Atmospheric Research (UCAR)",
	"UCAR Office of Programs (UOP)"
]

library_dc_fields = [
	"library_dc:recordID",
	"library_dc:dateCataloged",
	"library_dc:URL",
	"library_dc:issue",
	"dc:source",
	"dc:title",
	"library_dc:altTitle",
	"dc:creator",
	"dc:contributor",
	"dc:description",
	"dc:date",
	"library_dc:date_digitized",
	"dc:subject",
	"library_dc:instName",  # vocab 
	"library_dc:instDivision", # vocab
	"library_dc:libraryType", #vocab
	"dc:type",
	"dc:format",
	"dc:identifier",
	"dc:language",
	"dc:relation",
	"dc:coverage",
	"dc:rights",
	"dc:publisher",
]

webcat_fields = [
	"recordID",
	"url",
	"title",
	"itemType",
	"accessLevel",
	"accessionNum",
	"description",
	"fullTitle",
	"coverage",
	"creator",
	"contributor",
	"fullDescription",
	"subject",
	"publisher",
	"scientificDivision",
	"dateOfOriginal",
	"dateItemDigitized",
	"date",
	"source",
	"format",
	"identifier",
	"language",
	"copyright",
]

field_mapping = {
	"recordID" : "library_dc:recordID",
	"url" : "library_dc:URL",
	"title" : "dc:title",  ## if issue is present, peel it off and stick in issue, remainder goes to library_dc:altTitle
	"itemType" : "library_dc:libraryType",
	"accessLevel" : None,
	"description" : "dc:description",
	"fullTitle" : "dc:title", ## when present, becomes dc:title, else title becomes dc:title
	"coverage" : "dc:coverage",
	"creator" : "dc:creator",
	"contributor" : "dc:contributor",
	"fullDescription" : "dc:description",
	"subject" : "dc:subject",
	"publisher" : "library_dc:instName", ## no mapping? -> instName
	"scientificDivision" : "library_dc:instDivision",
	"dateOfOriginal" : "dc:date",
	"dateItemDigitized" : "library_dc:date_digitized",
	"date" : "dc:date",
	"source" : "dc:source",
	"format" : "dc:format",
	"identifier" : "dc:identifier",
	"language" : "dc:language",
	"copyright" : "dc:rights"
}

publisher_mapping = {

"National Oceanic And Atmospheric Administration (U.S.). Weather Research Program. Environmental Research Laboratories." :
	{	"instName" : "National Oceanic and Atmospheric Administration (NOAA)",
		"instDivision" : "Weather Research Program. Environmental Research Laboratories."},

"National Oceanic and Atmospheric Administration (U.S.). Weather Research Program. Environmental Research Laboratories." :
	{	"instName" : "National Oceanic and Atmospheric Administration (NOAA)",
		"instDivision" : "Weather Research Program. Environmental Research Laboratories."},

"National Center for Atmospheric Research (U.S.)" : 
	{	"instName" : "National Center for Atmospheric Research (NCAR)"},

"National Oceanic and Atmospheric Administration (U.S.). Environmental Research Laboratories" :
	{ 	"instName" : "National Oceanic and Atmospheric Administration (NOAA)",
		"instDivision" : "Environmental Research Laboratories" },

"Advanced Study Program" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)",
		"instDivision" : "Advanced Study Program (ASP)" },

"Mesoscale and Microscale Meteorology Division" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)",
		"instDivision" : "Mesoscale and Microscale Meteorology Division (MMM)" },

"National Center for Atmospheric Research (U.S.).  Balloon Facility" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },

"National Center for Atmospheric Research." :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },

"National Center for Atmospheric Research" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },

"Environmental and Societal Impacts Group" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)",
		"instDivision" : "Environmental and Societal Impacts Group (ESIG)" },

"National Center For Atmospheric Research (U.S.)." :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },
 
"National Center for Atmospheric Research (U.S)." :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },

"University Corporation for Atmospheric Research" :
	{	"instName" : "University Corporation for Atmospheric Research (UCAR)" },

"Scientific Computing Division" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)",
		"instDivision" : "Scientific Computing Division (SCD)" },

"Climate and Global Dynamics Division" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)",
		"instDivision" : "Climate and Global Dynamics Division (CGD)" },
 
"National Center for Atmospheric Research (U.S.)." :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },
 
"National Center for Atmospheric Research (U. S.)" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },

"Hawaii Institue of Geophysics." :
	{	"instName" : "Hawaii Institute of Geophysics" },

"National Center For Atmospheric Research (U.S.)" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)" },
 
"High Altitude Observatory" :
	{	"instName" : "National Center for Atmospheric Research (NCAR)",
		"instDivision" : "High Altitude Observatory (HAO)" }
}

