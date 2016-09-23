import os, sys

def getIdNum (myId):
	"""
	return the integer representation of a record or asset id or filename, e.g., 
	- "MONOGRAPH-000-000-000-747" -> 747
	- "asset-000-000-000-024" -> 024
	- "asset-000-000-000-024.pdf" -> 024
	"""
	
	base = os.path.splitext (myId)[0]
	numStr = ""
	for ch in base:
		if not ch.isdigit():
			continue
		if ch == '0' and not numStr:
			continue
		numStr += ch
	if not numStr:
		raise Exception, "could not get idNum from %s" % myId
	return numStr
		
def makeDrNum (num):
	return "DR%06d" % int(num)
	
def makeId (prefix, idNum):
	try:
		idNum = int (idNum)
	except:
		msg = "illegal accession #: '%s'" % accessionNum
		raise Exception, msg
	thousands = idNum / 1000
	## print "thousands: %d" % thousands
	ones = idNum % 1000
	## print "ones: %d" % ones
	id = "%s-000-000-%03d-%03d" % (prefix, thousands, ones)
	return id

def getPrefix (id):
	prefix = ""
	for ch in id:
		if ch != "0":
			prefix += ch
		else:
			break
	if prefix[-1] == '-':
		prefix = prefix[:-1]
	return prefix

# map prefix to collection
prefixMap = {
	'TECH-NOTE' : 'technotes',
	'MANUSCRIPT' : 'manuscripts',
	'ASR' : 'asr',
	'MONOGRAPH' : 'monographs',
	'HIST' : '1259799112473',
	'MLC' : 'mesalab',
	'NHRE' : '1254436054235'
}

def getCollectionFromId (id):
	prefix = getPrefix(id)
	if not prefixMap.has_key(prefix):
		raise KeyError, "prefixMap does not contain mapping for %s" % prefix
	return prefixMap[prefix]

