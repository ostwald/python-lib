"""
See https://docs.google.com/document/d/1P5AHWXWQzNFsZ9h6xzFaUMhv_-SzEZlBrDD2wKfzDqQ

1 - Read Yellowstone CVS file with fields:
last_name, first_name, username, acronym, charges

For each row
- use peopledb.searchInternalPerson to find upid
- insert upid in table
- write new .csv

"""
__author__ = 'ostwald'

import os, sys
from tabdelimited import CsvFile, CsvRecord
from ncar_lib.peopledb import InternalPerson

def get_upid (username):
	person = InternalPerson (username)
	if not person:
		raise ValueError, 'record not found for "%s"' % username
	return person['upid']

def update_data_with_pids():
	original_csv = '/Users/ostwald/devel/python/python-lib/opensky/report/NCAR users on Yellowstone.csv'

	user_data = CsvFile()
	user_data.read(original_csv)

	print '%d records' % len(user_data)
	for rec in user_data:
		try:
			upid = get_upid (rec['username'])
		except:
			print '- upid not found for %s: %s' % (rec['username'], sys.exc_info()[1])
			upid = ''
		# print ' - %20s %s' % (rec['username'], upid)
		# print ' - %s' % rec['charges']
		rec['upid'] = upid
		# print rec.asCsvRecord()
		print upid

	out_path = 'YELLOWSTONE_UPDATED.csv'
	user_data.write(out_path)
	print 'wrote to ', out_path

if __name__ == '__main__':
	update_data_with_pids()