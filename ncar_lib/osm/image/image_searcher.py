"""
IMAGe searcher - extends ReordGetter to search osm collections for IMAGEe authors

NOTE: jamaica and I met with XXXX, who is searching the PUBS database for at least one
particular author, and is using a pretty customized search to get the records he needs.
This indicates that whatever record we are able to extract using THIS method, there are
sure to be others that exist but must be hand-identified (somehow). But for now, see what
we can find ...

the goal is to search for IMAGe authors using xpath search fields
we'll have to decide which records to search, but for now search the WOS (osm) records ...

osm fields to search:
	/text//record/contributor,
	/text//record/creator
	
http://nldr.library.ucar.edu/schemedit/services/ddsws1-1?verb=Search&
	q=/text//record/contributors/person/lastName:Nychka+AND+/text//record/contributors/person/firstName:D&
	xmlFormat=osm&s=0&n=10&client=ddsws-explorer
	
"""
from UserDict import UserDict
from dds_client.search import RecordGetter, XmlRecord, XmlUtils, ServiceClient, URL
from ncar_lib.osm import OsmRecord
import image_authors


class ImageSearcher (RecordGetter):
	"""
	Performs a DDS search over the WOS collection in the NSDL Lib DCS for records
	having one or more IMAGe authors
	"""
	
	numToFetch = 1000000
	batchSize = 1000
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	
	def __init__ (self, lastName, firstName):
		self.lastName = lastName
		self.firstName = firstName
		q = "/text//record/contributors/person/lastName:%s" % lastName
		q += " AND /text//record/contributors/person/firstName:%s" % firstName[0]
		params = {
			"verb": "Search",
			"xmlFormat": "osm",
			"ky" :  "wos",
			"q":q
		}
		client = ServiceClient (self.baseUrl)
		RecordGetter.__init__ (self, client, params, OsmRecord)
		## print "before filter: %d records" % len(self.recs)
		
		# recs may not contain IMAGe authors, due to the way the DDS query is
		# perfromed. E.g., we searched for lastname and firstname, but we don't know
		# that the "hit" was produced by an author that matched both last and firstnames!
		# (one author may have matched lastName, while another may have matched Firstname)
		# so the filter makes sure that the records contain at least one or more IMAGe authors
		self.recs = filter (self.image_authors_filter, self.recs)
		
	def image_authors_filter (self, rec):
		"""
		returns true if there is an author in this record that matches both First and 
		LastNames with an IMAGe author
		"""
		return image_authors.nameMatcher.hasMatchInList (rec.getContributorPeople())
	
class ImageAuthorsTally (UserDict):
	
	def __init__ (self):
		UserDict.__init__ (self)
		self.load ()
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def load (self):
		for author_name in image_authors.author_names[0:]:
			splits = author_name.split()
			lastName = splits[-1]
			firstName = splits[0][0]
			searcher = ImageSearcher(lastName, firstName)
			# print getter.recs[3]
			print "%s - %d records found" % (author_name, len (searcher.recs))
			for rec in searcher.recs:
				id = rec.getId()
				if not self.has_key(id):
					self[id]=rec
					
	def report (self):
		print "found records for image authors"
		for id in self.keys():
			print id
		
def makeCitation (osmRec):
	s=[];add=s.append
	fields = ['title', 'pubName', 'volume', 'pages', 'id']
	for field in fields:
		add ("%s: %s" % (field, rec.get(field)))
	add ("pubDate: %s" % osmRec.getPubDate())
	add ("authors")
	for author in rec.getContributorPeople():
		add (str(author))
	return '\n'.join (s)
			
def tallyRunner ():
	tally = ImageAuthorsTally()
	tally.report()	
	
if __name__ == '__main__':
	lastName = "Rosenberg"
	firstName = "Duane"
	searcher = ImageSearcher (lastName, firstName)
	print "%d records found" % len(searcher.recs)
	for rec in searcher.recs:
		print '\n' + makeCitation (rec)
