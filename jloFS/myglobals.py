"""
working-repo - the base of the working directory - this provides material for update
reference-repo - the base of the reference directory - this gets updated
"""
import sys, os, re


host = os.getenv ("HOST")
platform = sys.platform
# print "\thost: %s\n\tplatform %s" % (os.getenv ("HOST"), sys.platform)

if host == 'acorn':
	# working_repo = "/dls/devel/ostwald/projects"
	# reference_repo = "/dls/devel/ostwald/projects/cvs"
	
	working_repo = "/home/ostwald/tmp/7-2-integrated-wrk/working/"
	reference_repo = "/home/ostwald/tmp/7-2-integrated-wrk/reference/"
	
	working = os.path.join (working_repo, "dlese-tools-project/src/org/dlese/dpc/schemedit/")
	reference = os.path.join (reference_repo, "dlese-tools-project/src/org/dlese/dpc/schemedit/")
	
elif host == 'dls-sanluis':
	working_repo = "/home/ostwald/projects"
	reference_repo = "L:/ostwald/projects"
	
	working = os.path.join (working_repo, "dlese-tools-project/src/org/dlese/dpc/schemedit/")
	reference = os.path.join (reference_repo, "dlese-tools-project/src/org/dlese/dpc/schemedit/")
	
elif host in ['taos', 'Taos.local']:
	working = "/Users/ostwald/devel/projects/dlese-tools-project/src/org/dlese/dpc/schemedit/"
	reference = "/Users/ostwald/devel/projects/cvs/dlese-tools-project/src/org/dlese/dpc/schemedit/"
	
	working_repo = "/Users/ostwald/devel/projects"
	reference_repo = "/Users/ostwald/devel/projects/cvs"

from UserDict import UserDict
class SortedUserDict (UserDict):
	
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
def _padStr (s, width, justify="left",  padchar=" "):
	# print "_padStr() width=%d" % width
	if len(s) > width:
		return s
		
	out = s
	
	for i in range (width - len(s)):
		if justify == 'left' or (justify == "center" and i%2):
			out = out + padchar
		elif justify == 'right' or justify == "center":
			out = padchar + out
		# print "%d/%s '%s' (%s)" % (i, width, out, justify)
	return out


def getIndent (level):
	indent = '   '
	if level == 0:
		return ''
	if level == 1:
		return indent
	foo = []
	for i in range(level):
		foo.append (indent)
	return '|'.join (foo)
	
def isdiff (p1, p2):
	print " ISDIFF "
	c1 = open (p1, 'r').read()
	c2 = open (p2, 'r').read()

	c1s = stripWhiteSpace (c1)
	c2s = stripWhiteSpace (c2)
	
	# print "c1 == c2 ? %s" % (c1s == c2s)
	return (c1s != c2s)

def stripWhiteSpace (s):
	out = ""
	pat = re.compile ("[\s]")
	for ch in s:
		if not pat.match (ch):
			out = out + ch
	return out

def filecmpTester ():
	relpath = 'dlese-tools-project/src/org/dlese/dpc/xml/schema/compositor/'
	filename = "InlineCompositor.java"
	working = os.path.join (working_repo, relpath, filename)
	reference = os.path.join (reference_repo, relpath, filename)
	filecmp (working, reference)
	
if __name__ == "__main__":
	filecmpTester()
		
