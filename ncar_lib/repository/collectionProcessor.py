import sys, os
from ncar_lib import OsmRecord
from xml_dec_repair import DeclarationFixer

osmdir = 'C:/Documents and Settings/ostwald/devel/dcs-instance-data/local-ndr/records/osm'

class CollectionProcessor:

	def __init__ (self, basedir, recordCallback):
		self.basedir = basedir
		self.process (recordCallback)

	def process (self, callback):
		print 'processing', self.basedir
		count = 0
		for i, filename in enumerate(os.listdir (self.basedir)):
			if not filename.endswith ('.xml'):continue
			path = os.path.join (self.basedir, filename)
			rec = OsmRecord (path)
			callback (rec)

		print "count: %d" % count
			
def astroPhysFix (rec):
	"""
	a function passed into CollectionProcessor as the recordCallback.
	it will be invoked on each OsmRecord in the collection
	"""
	pubName = rec.get ('pubName')
	if pubName == "Astrophysical Journal":
		print rec.getId()
		count = count + 1
		rec.set('pubName', 'The Astrophysical Journal')
		# print rec
		mypath = "c:/tmp/%s.xml" % rec.getId()
		rec.write (mypath)
		DeclarationFixer (mypath)
		
if __name__ == '__main__':
	for filename in os.listdir (osmdir):
		if filename[0] == '.':
			continue
		path = os.path.join (osmdir, filename)
		if not os.path.isdir (path):
			print "%s is not a dir" % filename
			continue
		CollectionProcessor(path, astroPhysFix)

