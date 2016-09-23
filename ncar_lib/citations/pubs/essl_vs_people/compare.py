"""
Things we might want to know:
	of those essl recs that have a upid,
	- how many peopleDBs can't be found by upid?
	- is the peopleDB always the same (or better) tahn essl info?

	of the records for which there is a person_id but not a upid,
	can we find a PeopleDB record??
"""

import sys
from EsslPeople import EsslPeopleSpreadsheet
from Person import EsslPerson, PeoplePerson

path = 'EsslPeopleDBdump.txt'
errors = []

for rec in EsslPeopleSpreadsheet (path):
	esslPerson = EsslPerson (rec)
	upid = rec.upid
	if not upid: continue
	try:
		peoplePerson = PeoplePerson (upid)
	except KeyError:
		errors.append (sys.exc_info()[1])
		continue
	diff = esslPerson.compare()
	if diff:
		print '\n%s  (%d)' % (upid, len(diff))
		for d in diff:
			print '\t%s' % str(d)
		
if errors:
	print "\nERRORS"
	for e in errors:
		print '\t', e
