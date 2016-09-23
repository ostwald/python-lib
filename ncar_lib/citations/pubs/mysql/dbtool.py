import sys
from PeopleDB import PeopleDB
from EsslPeopleDB import EsslPeopleDB

PERSON_ID = "person_id"
UPID = "upid"

PEOPLE_DB = "peopleDB"
ESSL_PEOPLE = "esslPeopleDB"

def getPeopleDBperson (upid):
	person = PeopleDB().getPerson (upid)
	if not person:
		print "\nnothing found for upid: %s" % upid
	else:
		print '\nPerson record from PeopleDB'
		print person
		return person

def getEsslPerson (field, id):
	person = None
	if field == UPID:
		person = EsslPeopleDB().getPersonByUpid (id)
	elif field == PERSON_ID:
		person = EsslPeopleDB().getPerson (id)
	if not person:
		print "\nnothing found for %s = %s: " % (field, id)
	else:
		print '\nPerson record from PeopleDB for %s = %s: " % (field, id)'
		print person
		return person
		
def getId (fieldname):
	id = raw_input ("enter a %s: " % fieldname)
	while (1):
		try:
			int(id)
			break
		except:
			id = raw_input ("%s must be an integer: " % fieldname)
	return id

def getEsslPersonField ():
	choices = ['1','2']
	prompt = """Select Database to Search:\n
	1. person_id (pubs internal)
	2. upid"""
	print prompt
	choice =  raw_input("your choice: ")
	while not choice in choices:
		choice = raw_input ("illegal response, try again: ")
	# Display the name entered by the user.
	if choice == '1': return PERSON_ID
	if choice == '2': return UPID
			
def getDatabase ():
	choices = ['1','2']
	prompt = """\nSelect Database to Search:\n
	1. PeopleDB
	2. essl_people"""
	print prompt
	choice =  raw_input("your choice: ")
	while not choice in choices:
		choice = raw_input ("illegal response, try again: ")
	# Display the name entered by the user.
	if choice == '1': return PEOPLE_DB
	if choice == '2': return ESSL_PEOPLE

def main():
	firstsearch = 1
	while (1):
		try:
			database = getDatabase()
			if database == PEOPLE_DB:
				getPeopleDBperson (getId(UPID))
			elif database == ESSL_PEOPLE:
				field = getEsslPersonField()
				getEsslPerson (field, getId(field))
			else:
				print "not implemented!"
				
		except KeyboardInterrupt:
			print "\ncancelled ...\n"
			break
			
		if raw_input ("\nsearch again (y/n)? ").lower() != 'y':
			sys.exit()

if __name__ == '__main__':
	main()

