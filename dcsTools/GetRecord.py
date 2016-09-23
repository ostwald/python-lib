from GetRecordClient import GetRecordClient

def getRecord (id, contextUrl):
	baseUrl = "http://%s/services/ddsws1-0" % contextUrl
	params = (
		('verb','GetRecord'),
		('id', id))
	adn = GetRecordClient (baseUrl)._getRecord (params)
	if adn:
		print "Success!"

id = "NSDL-000-000-000-068"
contextUrl = "www.nsdl.ucar.edu/ncs"

getRecord (id, contextUrl)

