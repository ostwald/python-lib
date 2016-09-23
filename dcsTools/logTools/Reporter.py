from Request import Request
from HyperText.HTML40 import *
from CatalinaLogTool import CatalinaLogTool, Filter, DateFilter
import re

class Reporter:

	columns = ("log_time", "id", "prior status", "current status", "lastEditor")
	report_path = "report.html"
	template_path = "template.html"

	def __init__ (self, logTool):
		self.logTool = logTool
		self.requests = logTool.requests

	def __len__ (self):
		return len (self.logTool)

	def requestToHtml (self, request):
		"""
		return a table row containing specified columns
		"""
		row = TR (klass="request-row")
		for col in self.columns:
			val = request.get_field(col)
			if not val:
				val = '&nbsp;'
			val_text = DIV (val, klass="request-field-text")
			row.append (TD (val_text, klass="request-field-cell"))
		return row.__str__()

	def _insertBody (self, html, body):

		patString = "<BODY>(.*?)</BODY>"

		pat = re.compile (patString, re.DOTALL)
		m = pat.search (html)
		if not m:
			raise "body NOT Found"

		return string.replace(html, m.group(), body)

	def showFilters (self):
		filter_display = DIV ()

		for filter in self.logTool.filters:
			filter_display.append (DIV (str(filter), klass="filter-text"))
		return filter_display

	def getBody (self):

		body = BODY()
		body.append (H1 ("Log File Reporter"))
		
		body.append (H3 ("Filters"))
		body.append (self.showFilters())

		body.append (H3 ("%d requests extracted" % len (self)))

		request_table = TABLE (klass="requests-table", cellspacing=1)
		header_row = TR (klass="header-row")
		for col in self.columns:
			header_text = DIV (col, klass="header-text")
			header_row.append (TD (header_text, klass="header-cell"))
		
		for request in self.requests:
			request_table.append (self.requestToHtml (request))
		body.append (request_table)

		return body

	def report (self):
		html = open (self.template_path, 'r').read()
		body = self.getBody().__str__()
		html = self._insertBody (html, body)

 		f = open (self.report_path, 'w')
 		f.write (html)
 		f.close()

		print html



if __name__ == "__main__":

	path = "catalina.out.sample"
	logTool = CatalinaLogTool (path)

	t1 = "Feb 2, 2006 9:42:32 AM"
	t2 = "Feb 10, 2006 9:42:32 AM"

 	## logTool.addFilter (DateFilter (t1,t2))
	logTool.addFilter (Filter ("isStatusEvent()"))
	## logTool.addFilter (Filter ("sessionId", "A09C651853EA6B440BA893F3CC68D1EB"))
	logTool.getRequests()

	reporter = Reporter (logTool)
	print reporter.report()
