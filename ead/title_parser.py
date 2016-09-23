"""
figure out how to parse the original titles from ead records and identify:
	dates
	names
"""
# 1 - get a list of titles
def getTitles ():
	from EadCollection import getBestCollection
	best = getBestCollection()
	return map (lambda x: x.title, best.getItems())

# 2 - save them so they're faster to work with
## not necesary
# 3 - parse into names and dates
import re
def getDates (s):
	# pat = "[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}" # finds all xx/mm/year
	pat = "[0-9/-]{3,50}"
	dateRegEx = re.compile (pat)
	# m = dateRegEx.search (s)
	# if m:
		# print "found: ", m.group()
	return re.findall (dateRegEx, s)
	
def getPeople (s):
	# pat = "[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}" # finds all xx/mm/year
	pat = "[A-Z][a-z]+, [A-Z][a-z]+"
	pRegEx = re.compile (pat)
	people = []
	for split in s.split(";"):
		m = pRegEx.match (split.strip())
		if m:
			people.append (m.group())
	return people	
	
# 4 - integrate with EadItem objects

def reportDates():
	s = "Appendix D; Letters of Support; Baker, D. James, 10/26/1992; Einaudi, Franco, 3/29/1993; Gordon, Arnold, 12/03/1993; Hallgren, Richard E., 10/26/1992"
	dates = getDates (s)
	if dates:
		print "%d dates found" % len(dates)
		for date in dates:
			print '\t', date
	else:
		print 'NO dates found'
		
def titlesWithDates():
	for title in getTitles():
		dates = getDates(title)
		if dates:
			print "\n%s" % title
			for d in dates:
				print "\t", d	
def titlesWithNoDates():
	for title in getTitles():
		dates = getDates(title)
		if not dates:
			print "\n%s" % title
if __name__ == '__main__':
	title = "Notepad; Washington, Warren; handwritten notes (n. d.)"
	people = getPeople (title)
	for p in people:
		print "\t", p
	

