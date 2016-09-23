""" 
But we realized that we care about something else.... since date will become
a required field, we are interested in how many records don't have a date. Do
not count dateRange as a date.

So if you can provide a spreadsheet of Records with No Dates and include the
same output of record id number, osm status and dcs status. That would be good.
I wonder if we can be do lucky as to be close to zero.
"""
import sys, os
from ncar_lib.repository import RepositorySearcher

class NoDateSearcher (RepositorySearcher):
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": 'osm',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid'],
			'q' : 'indexedXpaths:/record/coverage/date' 
			}
			
if __name__ == '__main__':
	searcher = NoDateSearcher()
	print '%d results' % len(searcher.results)
