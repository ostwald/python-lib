"""
scrape metadata and pdfs for leave nodes under target
"""
import os, sys
from technoteScraper import TechnoteScraper
from ncar_lib.webcat_scrape.WebCat import WebCat

def getMetadataUrls (url, collection, prefix):
	"""
	return a list of urls to submit to TechnoteScrapers
	"""
	destDir = "WebCatMetadata/%s" % collection
	if not os.path.exists (destDir):
		os.makedirs(destDir)
	cat = WebCat (url)
	node = cat.getNode (collection)
	leaves = cat.getLeaves (node)
	cat.hierarchy()
	count = len (leaves)
	urls = []
	for i, l in enumerate (leaves):
		# md = l.getMetadata(prefix)
		url = l.metadatapath
		msg = "%d/%d  %s" % (i, count, url)
		# print (msg)
		urls.append (url)
	return urls
		
if __name__ == '__main__':
	rootUrl = "http://library.ucar.edu/uhtbin/cgisirsi/Ids15V1HKy/SIRSI/116600007/503/8094"
	collection = "NCAR/TN-85+STR - A Microfilm atlas of magnetic fields in the solar corona."
	prefix = "TECH-NOTE"
	for url in getMetadataUrls (rootUrl, collection, prefix)[3:]:
		print "scraping " + url
		scraper = TechnoteScraper (url)
		scraper.write()
		scraper.getPdf()
		
