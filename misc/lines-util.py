import sys, os

"""
  dos ending: '\r\n' (\r is ^M is chr(13))

  unix ending: '\n' (chr (10)
"""

projects = "C:/Documents and Settings/ostwald/devel/projects"

# path = /dlese-tools-project/src/org/dlese/dpc/schemedit/CasaaServlet.java"

path = os.path.join (projects, "dcs-project/web/manage/create_collection_confirm.jsp")

def getContents (p):
	return open (p).read()

def writeContents (p, s):
	f = open(p, 'w')
	f.write (s)	

def dos2unix (p):
	s = getContents (p)
	s = s.replace (chr (13), '')
	writeContents (p, s)

def countDosEndings (p):
	s = getContents (p)
	## return s.count (chr (13)+ chr(10))
	return s.count ('\r\n')

if __name__ == "__main__":
	# print getContents (path)
	print "%d dos line endings" % countDosEndings (path)


