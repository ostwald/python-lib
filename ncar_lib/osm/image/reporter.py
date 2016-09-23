"""
Image reporter

find all records in WOS collection that have one or more contributers from the image_authors list

report as HTML
"""
from HyperText.HTML import *
from image_searcher import ImageSearcher, ImageAuthorsTally
from image_authors import nameMatcher

class OsmCitation:
	
	def __init__ (self, osmRec):
		self.osmRec = osmRec
		self.title = osmRec.get('title')
		self.pubName = osmRec.get('pubName')
		self.volume = osmRec.get('volume')
		self.volume = osmRec.get('volume')
		self.pages = osmRec.get('pages')
		self.pubDate = osmRec.getPubDate()
		self.id = osmRec.get('id')
		self.authors = osmRec.getContributorPeople()
		
	def getViewLink (self):
		url = 'http://nldr.library.ucar.edu/schemedit/browse/view.do?id=%s' % self.id
		return Href (url, self.id, target='dcs', title="view record in DCS")
		
	def __repr__ (self):
		s=[];add=s.append
		fields = ['title', 'pubName', 'volume', 'pages', 'id']
		for field in fields:
			add ("%s: %s" % (field, self.osmRec.get(field)))
		add ("pubDate: %s" % self.osmRec.getPubDate())
		add ("authors")
		for author in self.osmRec.getContributorPeople():
			add (str(author))
		return '\n'.join (s)
	
	def __cmp__ (self, other):
		"""
		how will lists of OsmCitations be sorted?
		"""
		return cmp (self.pubDate, other.pubDate)
		
	def asHtml (self):
		citation = DIV (klass="citation")
		citation.append (DIV (self.title, klass="title"))
		
		pubName = SPAN (self.pubName, klass="pubName")
		details = SPAN ("vol. %s, pp. %s (%s).  " % (self.volume, self.pages, self.pubDate))
		viewLink = SPAN (self.getViewLink(), klass='view-link')
		pubInfo = DIV(pubName, ".&nbsp;", details, " &nbsp; ", viewLink)
		
		citation.append (pubInfo)		

		# use list to present authors
		authors = DIV ("authors")
		authorList = UL (klass="author-list")
		for author in self.authors:
			lastName = author.lastName
			firstName = author.firstName
			authorHtml = LI ("%s, %s." % (lastName, firstName))
			if nameMatcher.hasMatch (lastName, firstName):
				authorHtml.update ({"klass":"image-author"})
			authorList.append (authorHtml)
			
		authors.append (authorList)
		citation.append (authorList)
		
		return citation

class Reporter:
	
	def __init__ (self, recs, outpath=None):
		self.recs = recs
		self.outpath = outpath or "html/report.html"
	
	def makeHtmlContent (self):
		contents = [];add=contents.append
		for rec in self.recs:
			add ("%s" % rec.asHtml ())
		return '\n\n'.join (contents)
		
	def makeHtmlDoc (self, outpath=None):
		
		head = open ("html/head.html", 'r').read()
		tail = open ("html/tail.html", 'r').read()
		
		html = "%s\n%s\n%s\n" % (head, self.makeHtmlContent(), tail)
		
		fp = open (self.outpath, 'w')
		fp.write (html)
		fp.close()
		print "wrote report to %s" % self.outpath
		
	def __repr__ (self):
		contents = [];add=contents.append
		for rec in self.recs:
			add ("%s" % rec)	
		return '\n\n'.join (contents)
		
	
	
def reporterTester ():
	contents = [];add=contents.append
	lastName = "Rosenberg"
	firstName = "Duane"
	searcher = ImageSearcher (lastName, firstName)
	
	osmCitationRecs = map (OsmCitation, searcher.recs)
	osmCitationRecs.sort()
	reporter = Reporter (osmCitationRecs)
	
	if 0:
		print reporter  # text
	elif 0:
		print reporter.makeHtmlContent() # html
	else:
		reporter.makeHtmlDoc()
	
		
def singleTester ():
	from ncar_lib.osm import OsmRecord
	rec = OsmRecord (path='OSM-000-000-000-001.xml')
	print OsmCitation (rec).asHtml()
		
def tallyReporter ():
	tally = ImageAuthorsTally()
	recs = map (OsmCitation, tally.values())
	recs.sort()
	reporter = Reporter (recs)
	reporter.makeHtmlDoc()
	
if __name__ == '__main__':
	# makeDoc (multipleTester())
	# singleTester()
	# reporterTester()
	tallyReporter()

