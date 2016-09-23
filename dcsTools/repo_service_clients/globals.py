import sys, os, string

ACORN = "acorn"
LOCALHOST = "localhost"
PREVIEW = "preview"

server = LOCALHOST

if server == PREVIEW:
	serverUrl = "http://preview.dpc.ucar.edu"
	collection = "ncc"
if server == ACORN:
	## serverUrl = "http://acorn:8688"
	serverUrl = "http://acorn.dls.ucar.edu:8688"
	collection = "xncc"
if server == LOCALHOST:
	# serverUrl = "http://localhost"
	serverUrl = "http://dls-sanluis.dls.ucar.edu"
	collection = "1201216476279"

baseUrl = serverUrl + "/schemedit/services/dcsws1-0"
# print "baseUrl: " + baseUrl


