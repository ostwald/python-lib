from ServiceClient import ServiceClient

def getRecord (id, contextUrl):
	baseUrl = "http://%s/services/ddsws1-0" % contextUrl
	params = (
		('verb','GetRecord'),
		('id', id))
	rec = ServiceClient (baseUrl, params).submit()
	if rec:
		print "Success!"
		return rec

id = "NSDL-000-000-000-068"
contextUrl = "www.nsdl.ucar.edu/ncs"

print getRecord (id, contextUrl)

