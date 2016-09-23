import os, sys

def getSourceDir ():
	host = os.getenv ("HOST") or os.getenv("COMPUTERNAME")
	platform = sys.platform
	# print "\thost: %s\n\tplatform %s" % (host, platform)
	
	if host:
		host = host.lower()
		if host == 'acorn' or host == 'oak':
			# return "/home/ostwald/asn-standards-docs/localized/science"
			# return "/home/ostwald/Documents/ASN/test"  ## just a few items
			return "/devel/ostwald/asn/2.0"
		if host.lower().startswith('taos'):
			return "/Documents/Work/DLS/ASN/mast-docs/"
			# return "/Documents/Work/DLS/ASN/standards-documents/v1.4.0/science/"
			# return "/Documents/Work/DLS/ASN/globe/"
		if host == 'mtsherman':
			return "/Users/jonathan/devel/python/asn/science/"
		if host == 'dls-pyramid':
			return "L:/asn/2.0"
		else:
			raise Exception, "Uknown Host: %s" % host

newYorkPath = os.path.join (getSourceDir(), "Science-1996-New York-Elementary Science, Intermediate Sc.xml")
coloradoPath = os.path.join (getSourceDir(), "Science-2007-Colorado-Model Content Standards Science.xml")
nsesPath = os.path.join (getSourceDir(), "Science-1995-National Science Education Standards (NSES)-National Science Education Standard.xml")

destDir = "/Library/WebServer/Documents/asn-globe/"

