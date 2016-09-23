
import sys, os
from StdDocumentHtml import StdDocumentHtml

stds = "/Users/ostwald/devel/python/asn/science"
html = "/Users/ostwald/devel/python/asn/html"

def showStdFiles ():
	for filename in os.listdir (stds):
		print filename
		
def stdToHtml (filename):
	src = os.path.join (stds, filename)
	asn = StdDocumentHtml (src)
	dst = os.path.join (html, os.path.splitext(filename)[0]+".html")
	print dst
	
	asn.write (dst)

if __name__ == "__main__":
	filename = "1995-Colorado-Science.xml"
	stdToHtml (filename)
