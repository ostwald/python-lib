import os, sys
from xls import WorksheetEntry, XslWorksheet

XslWorksheet.linesep = '\n'

def compare ():
	# reportbasedir = '/Users/ostwald/devel/python-lib/ncar_lib/repository/reports/lab_reports/reports'
	reportbasedir = '/home/ostwald/python-lib/ncar_lib/repository/reports/lab_reports/GCD-report'
	
	for filename in os.listdir(reportbasedir):
		root, ext = os.path.splitext(filename)
		if ext != '.txt':
			continue
		src = os.path.join (reportbasedir, filename)
		src_v1 = os.path.join (os.path.join (os.path.dirname(reportbasedir), 'GCD-report-5-2', filename))
		try:
			xls = XslWorksheet()
			xls.read(src)
			xls_v1 = XslWorksheet()
			xls_v1.read(src_v1)
			print "%s: xls: %d, xls_v1: %d" % (root, len(xls), len(xls_v1))
		except:
			print sys.exc_info()[1]
		
def report ():
	reportbasedir = '/home/ostwald/python-lib/ncar_lib/repository/reports/lab_reports/GCD-report'
	
	for filename in os.listdir(reportbasedir):
		root, ext = os.path.splitext(filename)
		if ext != '.txt':
			continue
		src = os.path.join (reportbasedir, filename)
	
		xls = XslWorksheet()
		xls.read(src)
		print "%s - %d" % (root, len(xls))
		
# report()
compare()
