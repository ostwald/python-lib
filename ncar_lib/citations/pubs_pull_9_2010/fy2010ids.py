"""
make a list of pubs_ids contained in the records (of Citation format) in specified directory
"""
import os, sys
from ncar_lib.citations import CitationReader

def getFY2010Ids ():
	basedir = '/home/ostwald/python-lib/ncar_lib/citations/pubs/PUBS_FY2010_metadata'
	ids = [];add=ids.append
	for filename in os.listdir (basedir):
		path = os.path.join (basedir, filename)
		reader = CitationReader(path=path)
		id = reader._get("pub_id")
		add (id)
	return ids
	
if __name__ == '__main__':
	for id in getFY2010Ids():
		print id
