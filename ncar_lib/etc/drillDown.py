import urllib
from webcatUtils import *

# url = "http://library.ucar.edu/uhtbin/cgisirsi/sYfxPvBlCW/SIRSI/106300008/503/993"
url = "http://library.ucar.edu/"
data = urllib.urlopen(url)
frontPageContent = data.read()

"""
    now we want to look for the "Digital Collections" link ...
    the link has a image with src='/WebCat_Images/English/Rootbar/White_blue/RBARCH.gif'
    and the "click handler" does some magic, including starting a new session.
    DON'T KNOW HOW WE CAN SIMULATE THIS ONE ...
"""

"""
    Lets say we just start with the "Content and Metadata Searching" page, which has a
	"View Collections" button at the top. By this point, we've already got our new session,
	and the button we need to click ("View Collections") has a simple URL.
	... what happens when we try to open this page in python??

"""
url = "http://library.ucar.edu/uhtbin/cgisirsi/4zJEXQ42kK/SIRSI/74070018/503/0/X/Content"
data = urllib.urlopen(url)
ContentAndMetadataSearchingContent = data.read()
# print ContentAndMetadataSearchingContent
"""
    Looks good! We can get the "NCAR Technical Reports Link"!!
	
"""
link = getLink ("NCAR Technical Reports", ContentAndMetadataSearchingContent)
if link:
	print link
else:
	raise Exception, "LinkNotFound for 'NCAR Technical Reports'"

data = urllib.urlopen (link.url)
NCARTechnicalReportsContent = data.read()
# print NCARTechnicalReportsContent

"""
    Now we want to go for the "NCAR Technical Notes" page, so repeat the above
	for this link ...
"""
link = getLink ("NCAR Technical Notes", NCARTechnicalReportsContent)
if link:
	print link
else:
	raise "LinkNotFound", "NCAR Technical Notes"

data = urllib.urlopen (link.url)
NCARTechnicalNotesContent = data.read()
# print NCARTechnicalNotesContent

"""
    and now we're on the page containing links to pages that will contain links to the actual
	reports. the links we're after now look like this:
	"NCAR Technical Notes 121-140" and we obtain them by calling getIndexItems ...
"""
links = getIndexItems (NCARTechnicalNotesContent)
for link in links:
	print link

"""
   OKAY - this is all well-and-good to here. now we have to read and parse a page with the actual
   notes on it ...
   see NotesItemsPage.py
"""
