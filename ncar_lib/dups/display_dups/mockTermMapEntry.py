"""
create a fake TermMapEntry
"""
import os, sys
from JloXml import XmlUtils
from titleTerms import Term
from dupTermMap import TermMapEntry

def makeTerm (title, docCount):
	element = XmlUtils.createElement ('term')
	element.setAttribute ('docCount', str(docCount))
	element.setAttribute ('termCount', '0') # we don't care about termCount
	XmlUtils.setText(element,title)
	return Term(element)
	
def makeTermMapEntry (key, terms):
	if type(terms) != type ([]):
		terms = [terms]
	entry = TermMapEntry (key)
	map (lambda x:entry.addTerm(x), terms)
	return entry
	
def getMockTermMapEntry ():
		
	terms = [
		makeTerm ("Weather impacts, forecasts, and policy - an integrated perspective", 1),
		makeTerm ("Weather impacts, forecasts, and policy:  an integrated perspective", 1),
		makeTerm ("Weather impacts, forecasts, and policy: An integrated perspective", 1)
	]
	
	key = "weatherimpactsforecastsandpolicyanintegratedperspective"
	termMapEntry = makeTermMapEntry (key, terms)
	# termMapEntry.report()
	return termMapEntry
