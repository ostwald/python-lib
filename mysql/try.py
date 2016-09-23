import MySQLdb
import string


class GoDataDataBase:
	def __init__ (self, server, user, passwd, db):
		self.server = server
		self.user = user
		self.passwd = passwd
		self.db = db

	def connection (self):
		return MySQLdb.connect(host=self.host, user=self.user,passwd=self.passwd, db=self.db)

	def __repr__ (self):

		print "host: ", self.host
		print "user: ", self.user
		print "db: ", self.passwd
		print "db: ", self.db		


class CopperDb (GoDataDataBase):
	server = "p50mysql63"
	host = "%s.secureserver.net" % server
	user = db = "jon0732704242167"
	passwd = "mjO052302"

	def __init__ (self):
		GoDataDataBase.__init__ (self, self.server, self.user, self.passwd, self.db)
	

class MyDb (GoDataDataBase):
	server = "p41mysql107"
	host = "%s.secureserver.net" % server
	user = db = "ostwald"
	passwd = "mjO052302"
	
	def __init__ (self):
		GoDataDataBase.__init__ (self, self.server, self.user, self.passwd, self.db)

def foo():

	db =  MySQLdb.connect( user="ostwald", db="test")
	cursor = db.cursor()
	table = "family"
	cursor.execute("SELECT * FROM %s" % table)
	for record in cursor.fetchall():
		s = [];add=s.append
		for field in record:
			add (str(field))
		print string.join (s, "\t")

if __name__ == "__main__":
	# print MySQLdb.__file__
	foo()
