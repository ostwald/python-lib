"""

- walkingLastEditorUpdater

	updates editor if the editor listed in the most recent status entry is obsolete. 
"""
import os, string
from nsdlToLdap_Globals import *
from DcsDataEditorUpdater import EditorUpdater, WalkingEditorUpdater
from dcsTools.user.nsdl_ldap_user_info import getLdapUserMapping


ldapUsernameMappings = getLdapUserMapping ("test_collection")

class LdapEditorUpdater (EditorUpdater):
	
	DO_WRITES = 1
	
	def getUsernameMappings (self):
		return ldapUsernameMappings
			
class LdapWalkingEditorUpdater (WalkingEditorUpdater):
	"""
	recursively visits an entire directory structure and update all the .xml
	files it finds
	"""
		
	UPDATER_CLASS = LdapEditorUpdater
				
			
def showUsernameMappings():
	for key in ldapUsernameMappings.keys():
		print "%s: %s" % (key, ldapUsernameMappings[key])

def test1 ():
	# path = os.path.join (DCS_DATA_DIR, 'msp2/1255996451551/PARI-000-000-000-001.xml')
	path = 'test_collection/TAAAS-000-000-000-001.xml'
	updater = LdapEditorUpdater (path)
		
if __name__ == "__main__":
	## baseDir = "test_collection"
	## baseDir = os.path.join (DCS_DATA_DIR, 'res_qual')
	# baseDir = os.path.join (DCS_DATA_DIR, 'res_qual')
	LdapWalkingEditorUpdater (DCS_DATA_DIR)
	test1()

