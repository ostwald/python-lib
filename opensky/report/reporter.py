"""
reporter creates a CSV file containing OpenSky resources
found for the yellowstone authors (who are listed in a spreadsheet)

- construct a list of author PIDs from spreadsheet
- query OpenSky for articles by these authors using OSWSClient
- create CVS file for each author (via OSWSResult)

There are 922 UPIDs
- we can't even construct a query with all of them!
	so we'll have to go through in batches ..
	make sure the batches will have a reasonable number of results to process (e.g., <1000)
- there are bounds to be tons of duplicate records, so
  maintain a map as we work through UPIDS
  - PID -> result


"""
__author__ = 'ostwald'

import sys, os
from opensky.osws_client import OSWSClient, OSWSResult
from tabdelimited import CsvFile, CsvRecord
from UserDict import UserDict

def normalize_charge(charge):
	"""
	util - convert charge string into a float
	"""
	charge = charge.replace(',','')
	try:
		return float(charge)
	except ValueError:
		# print 'could not normalize_charge for %s' % charge
		return 0

class YellowstoneAuthorData:

	cached_upid_path = 'data/cached_upids.txt'

	def get_upids (self):
		raise Exception, 'not implemented in abstract class'

class CachedAuthorData:

	def __init__ (self):
		self.upids = self.get_upids()

	def get_upids(self):
		lines = open(self.cached_upid_path, 'r').read().split('\n')
		return filter (None, map (lambda x:x.strip(), lines))

class AuthorDataSpreadSheet:
	"""
	We want to say what % of Yellowstone charges are associated with the NCAR Authors
	for each document. We need:
	- total charges
	- charge lookup for a given Author
	"""
	data_path = 'data/yellowstone_author_data.csv'


	def __init__(self):
		self.data = CsvFile()
		self.data.read (self.data_path)
		print '%d authors found' % len(self.data)
		self.chargeMap = self._get_charge_map()
		self.upids = self._get_upids()
		self.totalCharges = self._get_total_charges()

	def _get_charge_map(self):
		cmap = UserDict()
		for rec in self.data:
			cmap[rec['upid']] = normalize_charge(rec['charges'])
		return cmap

	def _get_upids(self):
		"""
		upids are keys of dict
		"""

		upids = filter (None, map (lambda x:x['upid'], self.data))
		print '%d upids found' % len(upids)
		return upids

	def get_charges(self, upid):
		upid = str(upid)
		if self.chargeMap.has_key(upid):
			return self.chargeMap[upid]
		else:
			print 'WARN: upid (%s) not in ChargeMap' % upid
			return 0

	def _get_total_charges (self):
		totalCharges = 0


		totalCharges = sum (map (lambda x:normalize_charge(x['upid']), self.data))
		return totalCharges

	def cache_upids():
		"""
		just by chance we want cashe the upids, e.g., to populate data for CachedAuthorData
		"""
		upids = self.get_upids()
		fp = open (self.cached_upid_path, 'w')
		fp.write ('\n'.join(upids) + '\n')
		fp.close()

# --------------



class Reporter(UserDict):

	UPID_BATCH_SIZE = 50
	dowrites = 1

	# headers = [
	# 	'pid', # for debugging
	# 	'pub_type',
	# 	'pub_date',
	# 	'title',
	# 	'authors',
	# 	'doi',
	# 	'ark',
	# 	'journal',
	# 	'collaboration'
	# ]

	def __init__(self):
		self.data = {}
		self.author_data = AuthorDataSpreadSheet()
		self.upids = self.author_data.upids

		self.osws_client = OSWSClient ()

	def process(self):
		BATCH_THROTLE = None #cut process short (e.g., for debugging)
		print 'PROCESSING ...'
		for i in range(0, len(self.upids), self.UPID_BATCH_SIZE):
			if BATCH_THROTLE and i >= BATCH_THROTLE:
				break
			print '- %d' % i
			self.process_batch(i)

		# self.process_batch(0)
		print '%d resources to report' % len(self.keys())
		if self.dowrites:
			self.write_report()

	def process_batch(self, start):
		"""
		process a batch uf upids - if our batch is too big the return sets get out of hand.
		Of course this depends on the data, but for the case of Yellowstone authors,
		a batch size of 100 will return more than a thousand results.

		side-effect - populate Reporter.data, a dict that maps from pid to table-entry
		"""
		end = min(start+self.UPID_BATCH_SIZE, len(self.upids)-1)
		query = self.get_upid_query(self.upids[start:end])

		#decorate query
		# do we want to restrict by genre?
		query = '(%s) AND genre:"article"' % query

		## We also want to restrict DATES 2006-2015 inclusive?
		query += " AND date:[2006-01-01T00:00:00.000Z TO 2015-12-31T00:00:00.000Z]"
		# print query
		params = {
			'start' : '0',
			'rows' : '1000',
			'output' : 'xml',
			'q' : query
		}

		results = self.osws_client.getResults(params)

		print ' ... %d found in repo' % results.numFound

		for result in results:
			# result is a OSWSResult instance, we can update some slots ...
			ncar_authors = result.ncar_authors
			other_ncar_authors = []
			yellowstone_authors = []
			for author in ncar_authors:
				if author.upid in self.author_data.upids:
					yellowstone_authors.append(author)
				else:
					other_ncar_authors.append(author)


			y_author_upids = map(lambda x:x.upid, yellowstone_authors)
			result.yellowstone_authors = '; '.join(map(lambda x:x.displayName, yellowstone_authors))
			result.num_yellowstone_authors = len(yellowstone_authors)
			result.other_ncar_authors = '; '.join(map(lambda x:x.displayName, other_ncar_authors))
			result.sum_author_charges = sum (map (lambda x:self.author_data.get_charges(x), y_author_upids))
			self[result.pid] = result.toCsv()

	def get_upid_query (self, upids=None):
		"""
		creates a solr query clause that ORs the upids specified
		will find all documents associated with any of provided pids
		"""
		upids = upids or self.upids
		clauses = map (lambda x:'upid:"%s"' % x, upids)
		return ' OR '.join(clauses)

	def write_report(self):
		outpath = "REPORTER_TEST.csv"
		fp = open(outpath, 'w')
		sorted_keys = self.keys();sorted_keys.sort()
		fp.write(','.join(OSWSResult.headers) + '\n')
		for pid in sorted_keys:
			fp.write(self[pid].encode('utf-8') + '\n')
		fp.close()
		print 'wrote report to %s' % outpath

# tester = results[0]
# # print tester
# tester.report()
# print tester.toCsv()

def authorDataTester():
	ss = AuthorDataSpreadSheet()
	print 'total charges: %s (%s)' % (ss.totalCharges, type (ss.totalCharges))
	upid = 24793
	print 'charges for %d is %f' % (upid, ss.get_charges(upid))

if __name__ == '__main__':
	rptr = Reporter()
	rptr.process()

