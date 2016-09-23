"""
global contants and functions

repository - path to the records baseDir - this is where records are written
templateDir - path to directory containing templates for use in constructing XML records

"""
import os

repository = None
templateDir = None

if 0:# taos
	repository = '/Users/ostwald/devel/backpack-data/records'
else:
	# acorn
	repository = '/home/ostwald/Documents/NSDL/Backpack/ingest/repository'
	templateDir = '/home/ostwald/python-lib/backpack/templates'

def getNextIdNum (path):
	"""
	get the next ID for the directory at path, 
		based on the ids of the existing files there
	"""
	maxNum = 0
	for filename in os.listdir(path):
		recNum = makeRecNum (filename)
		maxNum = max (maxNum, recNum)
	return maxNum + 1
	
def makeRecNum (filename):
	"""
	extract the record number from a filename by
	collecting the digits and turning into an int
	"""
	digits = ''
	for ch in os.path.splitext(filename)[0]:
		if ch.isdigit():
			digits += ch
	return int(digits)
	
if __name__ == '__main__':
	# print makeRecNum ('askasd-adsu-000-000-005-67')
	print getNextIdNum ('/Users/ostwald/devel/backpack-data/records/concepts/concepts_bp/')
