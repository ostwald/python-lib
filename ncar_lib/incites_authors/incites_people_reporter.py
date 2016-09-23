"""
"""
import os, sys
from UserList import UserList
from find_person import PersonFinder, resolveFullName
from data_filter import FilteredAuthorData
from HyperText.HTML40 import *
from html import HtmlDocument

class InCitesAuthorInfo:
	
	def __init__ (self, id, finder, matches):
		"""
		names are derived from inCitesAuthor data
		matches come from peopleDB
		"""
		self.id = id
		# self.inCitesName = fullname
		for attr in ['fullname', 'firstName', 'middleName', 'lastName', 'note']:
			setattr (self, attr, getattr (finder, attr))
		self.matches = matches
		self.numMatches = len(matches)

class SimpleReporter (UserList):
	def __init__ (self):
		self.data = []
		self.recordsToReport = 10
		self.errors = []
		self.notes = []
		self.people = FilteredAuthorData().people # UniquePeople	
		# self.report()
		self.getAuthorMatchInfo()
		
	def getAuthorMatchInfo (self):
		person_counter = 1
		max_count = self.recordsToReport or len(self.people.keys())
		for fullname in self.people.keys()[:max_count]:
			try:
				finder = PersonFinder (fullname)
				candidates = finder.candidates

				id = 'author-%d' % person_counter
				person_counter += 1
					
				# print 'processing authorInfo for ' + fullname
				authorInfo = InCitesAuthorInfo (id, finder, candidates)
				self.append(authorInfo)
				
			except KeyError, e:
				print 'ERROR', e
				self.errors.append(fullname + ": " + str(e))

		
	def report(self):
		for authorInfo in self:
			try:
				if authorInfo.numMatches == 1:
					continue
					
				if authorInfo.note:
					self.notes.append(authorInfo.note)
					
				## print '\n%s (%d)' % (fullname, size)
				print "\n%d candidates found for '%s' (%s | %s)" % \
					(len(authorInfo.matches), 
					 authorInfo.fullname, 
					 authorInfo.lastName, 
					 authorInfo.firstName)
					 
				for person in authorInfo.matches:
					print '- ', person
			except Exception, e:
				self.errors.append(authorInfo.fullname + ": " + str(e))
			
	def showErrors (self):
		if self.errors:
			print '\nNames that could not be parsed'
			for error in self.errors:
				print error
		else:
			print '\nAll names were parsed'

	def showNotes(self):
		if self.notes:
			print '\nNotes'
			for note in notes:
				print note		
		else:
			print '\nNo notes generated'
		
class HtmlReporter (SimpleReporter):
	
	results_columns = ['numMatches', 'inCitesName', 'peopleDBlink']
	
	def __init__ (self):
		SimpleReporter.__init__ (self)
		self.htmlDoc = None
		print '%d authorInfo instances' % len(self.data)
		
		
	def asHtmlDoc (self):
		if self.htmlDoc is None:
			mockup_link = Href ("../reporter-mockup.html", 'to Mockup')
			reportTable = self.makeReportHtml()
			javascript = [
				'javascript/prototype.js',
				'javascript/scriptaculous-js-1.9.0/scriptaculous.js',
				'javascript/toggler.js',
				'javascript/decorate_upids.js'
			]
				
				
			self.htmlDoc = HtmlDocument(mockup_link,
								   reportTable,
								   title="inCites Author Reporter",
								   stylesheet="styles.css",
								   javascript=javascript)
		return self.htmlDoc
	
	def getInCitesAuthorInfo (self, authorInfo):
		"""
		make the html for a inCitesAuthor & its matches
		"""
		print 'getInCitesAuthorInfo with ' + authorInfo.fullname
		id = authorInfo.id
		
		togglerClass = authorInfo.matches and "toggler" or ""
		
		toggler = DIV (id=id, klass=togglerClass)
		
		if authorInfo.numMatches > 0:
			togglerLnkClass = "inCitesAuthor togglerClosed"
		else:
			togglerLnkClass = "inCitesAuthor noTogglerClosed"
		# print "%s %s" % (authorInfo.inCitesName, authorInfo.numMatches)
						  
		togglerLnk = DIV(id='toggler-lnk-'+id, klass=togglerLnkClass)
		toggler.append(togglerLnk)
		
		authorTable = TABLE(klass="authorTable")
		togglerLnk.append(authorTable)
		matchesContent = '(%d matches)' % authorInfo.numMatches
		authorTable.append(
			TR(
				TD (authorInfo.fullname, klass="author"),
				TD (matchesContent, klass="matches")
			)
		)

		if authorInfo.numMatches > 0:
			togglerCon = DIV(id='toggler-con-'+id, style="display:none")
			toggler.append(togglerCon)
			matchTable = TABLE(klass="matchTable")
			togglerCon.append(matchTable)
			
			for match in authorInfo.matches:
				match_row = TR (klass="peopleDBmatch", id=match.upid)
				match_row.append (
					TD (match.getName(), klass="match-name"),
					TD (match.upid, klass="match-upid"))
				matchTable.append(match_row);
		return toggler
		
	def makeReportHtml (self):
		report = DIV (id='reportTable')
		person_counter = 1
		max_count = self.recordsToReport or len(self.people.keys())
		
		for authorInfo in self:
			# print authorInfo.fullname, authorInfo.numMatches
			try:
				if authorInfo.numMatches == 1:
					continue
					
				if authorInfo.note:
					self.notes.append(authorInfo.note)
					
				# print 'processing authorInfo for ' + fullname
				report.append (HR (klass="divider"))
				report.append(self.getInCitesAuthorInfo (authorInfo))

			except Exception, e:
				self.errors.append(authorInfo.fullname + ": " + str(e))
		return report
		
	def writeHtmlDoc (self, path=None): 
		path = path or "report_html/INCITES_REPORT.html"
		fp = open (path, 'w')
		fp.write (self.asHtmlDoc().__str__())
		fp.close()
		print "wrote to " + path

if __name__ == '__main__':
	# findPeople()
	if 0:
		reporter = SimpleReporter()
		reporter.report()
	if 1:
		reporter = HtmlReporter()
		print reporter.asHtmlDoc()
		# reporter.writeHtmlDoc()
	reporter.showErrors()
	reporter.showNotes()
	# print reporter.asHtmlDoc()
