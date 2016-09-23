import string, math, os, sys

from JloXml import AdnRecord

class RecordMaker:

	def __init__ (self):

		if sys.platform == 'win32':
			records_path = "L:/ostwald/records/mother-records"
		else:
			records_path = "/devel/ostwald/records/mother-records"
		template_path = os.path.join (records_path, "adn/comet/COMET-6.xml")
		collection_key = "fake50000"
		rec = AdnRecord (path=template_path)
		coll_dir = os.path.join (records_path, "adn/" + collection_key)
		prefix = "FAKE-50000"
		
		for i in range (1,50001):
			id = self.makeId (prefix, i)
			rec.setId (id)
			filename = id + ".xml"
			rec.write (os.path.join (coll_dir, filename))


	def makeId (self, prefix, n):
		nStr = "%09d" % n
		return "%s-%s-%s-%s" % (prefix, nStr[:3], nStr[3:6], nStr[6:])


if __name__ == "__main__":
	RecordMaker()
		




