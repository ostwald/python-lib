"""
NOT USED!!
"""
import os, sys
from ncar_lib.repository import RepositorySearcher, SummarySearcher

class notFY2010Searcher (RepositorySearcher):
	"""
	find all records in not-fy2010 that don't have rights/coverage
	"""
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		collection = 'not-fy10'
		return {
			"verb": "Search",
			"ky": 'not-fy10',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
			
class notFY2010Summarizer (SummarySearcher):
	"""
	find all records in not-fy2010 that don't have rights/coverage
	"""
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		collection = 'not-fy10'
		return {
			"verb": "Search",
			"ky": 'not-fy10',
			'facet' : 'true',
			'facet.field' : '/key//record/rights/copyrightNotice',
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
			
	def report (self):
		summary = self.summary
		print "\nSUMMARY"
		print "%d records found" % summary.totalNumResults
		for faceted_field in summary.faceted_fields:
			faceted_field.report()

if __name__ == '__main__':
	if 0:
		searcher = notFY2010Searcher()
		print "%d results" % len(searcher)
	else:
		summarizer = notFY2010Summarizer()
		summarizer.report()
