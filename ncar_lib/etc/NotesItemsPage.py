import os
import urllib
from webcatUtils import *

## url = "http://library.ucar.edu//uhtbin/cgisirsi/CywqhcdTvV/SIRSI/301540023/503/6866"
## data = urllib.urlopen(url)
## content = data.read()
## print content

"""
the stuff we're interested in follows the title of this page, which follows
it's ancestors in the heirarchy, e.g.,
NCAR Technical Reports
  NCAR Technical Notes
    NCAR Technical Notes 1-20
	  Doc 1 (icon, content-link)
	  Doc 2 (icon, content-link)
	  ....
	  Doc n  (icon, content-link)

icon can be either a folder ("FOLDER.gif") or issue ("ISSUE.gif")
- if it is a FOLDER, then the icon(folder) link leads to some metadata about the items,
  and the content-link leads to a page on which are the PARTS, each with metadata.
- if it is an ISSUE, the icon link leads to metadata, and the content link leads to the pdf.
"""

class TechNoteIcon:
	def __init__ (self, source):

		elementPat = re.compile ("<A HREF=([\S]+?)>[\s]+?<IMG SRC=\"([\S]+?)\".*?></A>", re.S)
		m = elementPat.search (source)
		if not m:
			print source
			raise Exception, "Icon not found"
		self.path = m.group(1)
		filename = os.path.split (m.group(2))[1]
		self.type = filename.split(".")[0]

	def __repr__ (self):
		return "%s: %s" % (self.type, self.path)

class TechNoteLink:
	def __init__ (self, source):
		elementPat = re.compile("<A HREF=\"([\S]+?)\">([^>]*?)</A>", re.S)
		m = elementPat.search (source)
		if not m:
			print source
			raise Exception, "Link not found"
		self.path = m.group(1)
		self.label = m.group(2).strip()

	def __repr__ (self):
		return "%s (%s)" % (self.label, self.path)
	
class TechNoteEntry:
	"""
	represents the icon and textual link that appear together as an entry for a tech note
	"""

	def __init__ (self, source):
		self.source = stripComments (source).strip()
		self.icon = TechNoteIcon (source)
		self.link = TechNoteLink (source)

	def __repr__ (self):
		return "%s (%s)" % (self.link.label, self.icon.type)

class Page:

	def __init__ (self, url=None, content=None):
		if url:
			self.url = url
			data = urllib.urlopen(url)
			self.content = data.read()
		else:
			if not content:
				raise "UrlOrContentRequired"
			self.content = content

	def process (self):
		"""
		find the link for "NCAR Technical Notes n-nn" and only look
		at the remainder.

		we cheat by finding the following comment string:
		 <!-- Print the children nodes -->
		"""
		marker = "<!-- Print the children nodes -->"
		x = self.content.find (marker)
		if x < 0:
			raise Exception, "Marker not found"

		# chop also everything after the table end
		buffer = self.content[x:]
		x = buffer.find ("</TABLE>")
		if x < 0:
			raise Exception, "End Table tag expected but not found"
		buffer = buffer[:x]
		
		# print buffer

		# now grab all the table cells with content
		technotes = []
		cellpat = re.compile ("<TD[^>]*?>(.*?)</TD>", re.S)
		cells = cellpat.findall (buffer)
		# print "%d cells found" % len(cells)
		for c in cells:
			if c.strip():
				
				cellcontent = stripComments (c).strip()
				technotes.append (TechNoteEntry (c))
				print technotes[-1]

		return technotes

if __name__ == "__main__":

	path = "notesItemsPage.html"
	page = Page (content=open(path).read())
	# page.stripComments()
	page.process()
	
		
