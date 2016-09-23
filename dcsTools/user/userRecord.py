
import os, sys
from JloXml import MetaDataRecord, XmlUtils

userdir = "C:/Program Files/Apache Software Foundation/Tomcat 5.5/var/dcs_conf/users"

class UserRecord (MetaDataRecord):
	
	xpath_delimiter = "/"
	id_path = '/record/username'
	DO_WRITES = 1
	
	def getUserName (self):
		return self.getTextAtPath ("username")
		
	def setUserName (self, value):
		return self.setTextAtPath ("username", value)

	def changeUserName (self, newname):
		## make sure there is not another user record for this name
		newfilename = newname + ".xml"
		dirname = os.path.dirname (self.path)
		if newfilename in os.listdir (dirname):
			raise NameError, "new file name (%s) already exists" % newfilename
		self.setUserName (newname)
		dst = os.path.join (dirname, newfilename)
		if self.DO_WRITES:
			self.write()
			os.rename (self.path, dst)
			print "moved to %s" % dst
		else:
			print "WOULD HAVE written and moved to %s" % dst
		
		
if __name__ == '__main__':
	path = os.path.join (userdir, "fooberry.xml")
	rec = UserRecord(path=path)
	rec.changeUserName ("jonathan")
