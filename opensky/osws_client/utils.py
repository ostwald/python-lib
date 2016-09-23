import sys, os
from client import OSWSClient

__author__ = 'ostwald'

def getResult (pid):
	query = 'PID:"%s"' % pid
	# baseUrl = 'http://cypressvm.dls.ucar.edu:8788/osws/search/v1'
	params = {
		'start' : '0',
		'rows' : '1',
		'output' : 'xml',
		'q' : query
	}

	client = OSWSClient ()
	results = client.getResults(params)
	if len(results) != 1:
		raise Exception, 'Did not get a single result for pid:%s' % pid
	return results[0]

def strip_blank_lines (s):
	outlines=[];add=outlines.append
	# for line in s.split('\n'):
	lines = filter (None, map (lambda x:x.strip(), s.split('\n')))

	return '\n'.join(lines)

def get_result_tester():
	pid = 'conference:2777'
	result = getResult (pid)
	print result.toCsv()

def strip_tester():
	path = 'xml_samples/osws-response-sample.xml'
	xml = open(path).read()
	print strip_blank_lines(xml)


def getMods (pid):
	pass

if __name__ == '__main__':
	strip_tester()
