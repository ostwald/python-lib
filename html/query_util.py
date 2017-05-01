import sys, os, re
from urlparse import urlparse, parse_qs

# parse = urlparse(url)

#print parse.query
# print '\n\n'

# params = parse_qs(parse.query)



class QueryUtil:
	
	def __init__ (self, url):
		self.url = url
		self.parse = urlparse(url)
		self.params = parse_qs(self.parse.query)
		self.path = self.parse[2]
	
	def report (self, params=None):
		if params is None:
			params = self.params
		for key in self.params:
			#  print '%s (%s)' % (key, type (params[key]))
			print '\n- %s' % key
			for item in self.params[key]:
				print ' - %s' % item

	def getParameter (self, param):
		val = self.params[param]
		if val is None or len(val) == 0:
			return None
		if len(val) == 1:
			return val[0]
		return val
				
	def makeQueryStr (self, params=None, filterFn=None):
		queryList = []
		if params is None:
			params = self.params
		if filterFn is None:
			filterFn = lambda x: 1  # returns everything
		for key in filter (filterFn, self.params.keys()):
			for val in self.params[key]:
				paramStr = "%s=%s" % (key, val)
				queryList.append (paramStr)
		return '&'.join(queryList)
			
if __name__ == '__main__':
	url = """http://foo.com/foo?facet=on&facet.field=/key//record/contributors/person/affiliation/instDivision&facet.field=/key//record/coverage/date/@type&facet.field=/relation.memberOfCollection//key//collectionRecord/additionalMetadata/collectionRecord/key&facet.field=/key//record/general/pubName/@type&facet.field=/key//record/general/title/@type&facet.field=/key//record/classify/classification&facet.field=/key//record/classify/collaboration&verb=Search&ky=info&ky=technotes&ky=monographs&ky=manuscripts&ky=asr&ky=staffnotes&ky=mesalab&ky=ncar-books&ky=scd&ky=osgc&ky=soars&ky=image&ky=wwashington&ky=vinlally&ky=natlballoonfac&ky=jkuettner&ky=gate&ky=scdnewsletter&ky=nhre&ky=unav&ky=unhistory&ky=hao&ky=dls&ky=wsw&ky=ipcc&ky=atd&ky=srm&ky=ucar&ky=twerle&ky=siparcs&ky=comm&ky=wor&ky=lie&ky=unpc&ky=ams&ky=unoh&dcsStatus=Done&s=0&n=20"""
	qu = QueryUtil(url)
	# qu.report()
	
	myParams = qu.params
	
	print '\nMY_PARAMS'
	qu.report(myParams)
	
	del (myParams['ky'])
	
	print qu.makeQueryStr(myParams)
