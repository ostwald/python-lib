from UserDict import UserDict
from UserList import UserList

path = 'EsslPeopleDBdump.txt'

class PersonTable (UserDict):
	
	def __init__ (self, path):
		UserDict.__init__ (self)
		s = open(path).read()
		lines = s.split('\n')
		print '%d lines read' % len(lines)
		self.schema = lines[0].split('\t')
		print self.schema
		recs = lines[1:]
		print '%d data read' % len(recs)
		
		for line in recs:
			personRec = PersonRec (line, self.schema)
			self[personRec.person_id] = personRec
			
			
class PersonRec:
	
	def __init__ (self, data, schema):
		self.schema = schema
		self.data = data.split('\t')
		
		for i, field in enumerate (schema):
			setattr (self, field, self.data[i])
			
	def __repr__ (self):
		return str (self.data)
			
if __name__ == '__main__':
	people = PersonTable (path)
	rec = people['100015']
	print rec
	
		
