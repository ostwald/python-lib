import sys,os
from EadCollection import getBestCollection
from EadFoundation import getEadRecord
from JloXml import XmlRecord

## def getBoxes (collection):
			
## use with no
schemaUri = "http://www.dls.ucar.edu/people/ostwald/Metadata/at_ead/record.xsd" 
prefix = 'BEST'
outdir = 'best'
dowrite = 1

def bestXml ():
	best = getBestCollection()
	for item in best.getItems():
		xml = item.asXml(prefix)
		# print "-------------\n%s\n---------------" % xml.toxml()
		rec = XmlRecord (xml=xml.toxml())
		rec.setSchemaNamespace ()
		rec.setNoNamespaceSchemaLocation (schemaUri)
		print "-------------\n%s\n---------------" % rec
		filename = item.getRecordId (prefix) + ".xml"
		outpath = os.path.join (outdir, filename)
		try:
			if dowrite:
				# fp = open (outpath, 'w')
				# fp.write (xml.toxml())
				# fp.close()
				rec.write (outpath)
				print "wrote %s" % filename
			else:
				print rec
		except:
			print "failed with " + item.id
			print sys.exc_info()[0], sys.exc_info()[1]
	
def tester ():
	path = "Final Washington EAD.xml"
	ead = getEadRecord()
	item = ead.getItem ("ref72")
	print item.asXml("FOOD").toprettyxml()
	
if __name__ == "__main__":
	bestXml()
