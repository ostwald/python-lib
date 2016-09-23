from suds.client import Client
import logging
from misc.dumpObj import dumpObj

"""
despite being documented in https://fedorahosted.org/suds/wiki/Documentation,
i can't import suds.plugin, which seemed to be the best hope for grabbing the
xml response, which apparently is necessary for obtaining a Document from the
service - ARGGGG
"""
# from suds.plugin import Plugin 

"""
# bogus cause we can't get hold of Plugin
class MyPluggin (Plugin):
	def received (context):
		print context
"""

url = 'http://www.jesandco.net/asn/asnwebservice/acsrservice.asmx?wsdl'

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


def getSimpleClient ():
	return Client(url)

def getFancyClient ():
	"""
	i THOUGHT this was the soln to my troubles trying to print
	out the xml returned but i because i can't
	from suds.plugin import Plugin
	this is bogus
	"""
	return Client (url, plugins=[MyPluggin])

# print client

def getJurisdictions():
	result = getSimpleClient().service.GetJuris()

	print result.asn_ACSRJurisdictions

def getSubjects():
	result = getSimpleClient().service.GetSubj()

	print result

def getDocuments ():
	Jurisdiction="CO"
	Subject = "Science"
	print getSimpleClient().service.GetDocuments(Jurisdiction="CO", Subject = "Science")


def getAPPDocuments():
	"""
	get a "APP document" using an ID like: '00a6d3fc-0cad-4048-bafa-bc0be9d2c2cd'
	
	NOTE: this is NOT the same form of ASN Doc that we are used to working with!
	"""
	# id = 'http://purl.org/ASN/resources/D100003B'
	id='00a6d3fc-0cad-4048-bafa-bc0be9d2c2cd'
	# id = 'D100003B'
	result = getSimpleClient().service.GetAPPDocuments(DocumentID=id)
	# from misc.dumpObj import dumpObj
	# dumpObj(result)
	print result


def getACSRDocument():
	"""
	Get an ASN Document (using DocumentID which is NOT the same as the purl form!)
	"""
	id='00a6d3fc-0cad-4048-bafa-bc0be9d2c2cd'
	# id='D100027B'
	result = getSimpleClient().service.GetACSRDocument(DocumentID=id)
	from misc.dumpObj import dumpObj
	# dumpObj(result.RDF)

	return  result

def asnResolver (lookupText):
	"""
	gives us just what the REST base resolver would, given a 
	- PURL, StatementID (sid), or DocumentID)

	NOTE: Seems only to give responses for doc or standard ids
	"""
	result = getSimpleClient().service.ASNResolver (LookupText=lookupText)

def getSearch (searchString=None, jurisdiction=None, subject=None, sid=None):
	"""
	providing just searchString causes SQL errors at server!
	"""
	result = getSimpleClient().service.GetSearch (Searchstring=searchString,
												  Jurisdiction=jurisdiction, Subject=subject, SID=sid) 

if __name__ == '__main__':
	# getJurisdictions()
	# getSubjects()
	# getAPPDocuments()
	# asnResolver('http://purl.org/ASN/resources/D100003B')
	# getACSRDocument()
	# getSearch (jurisdiction = "CO", searchString="knowledge")
	getDocuments()
