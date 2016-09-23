"""

- UCAS DcsDataEditorUpdater

	updates this record to change occurance of editors that need to be changed
	according to the userMapping. 
"""
import os, string
from nsdlToLdap_Globals import *
from DcsDataEditorUpdater import EditorUpdater, WalkingEditorUpdater
from dcsTools.user.ucas_user_info import getUcasUserMapping
# from dcsTools.user.nsdl_ldap_user_info import getLdapUserMapping

UCAS_DIR = '/home/ostwald/Documents/NCAR Library/Transition to UCAS' # acorn

userdirname = os.path.join (UCAS_DIR, 'users')
ucasUsernameMappings = getUcasUserMapping (userdirname)

class UcasEditorUpdater (EditorUpdater):
	
	DO_WRITES = 0
	
	def getUsernameMappings (self):
		return ucasUsernameMappings
			
class UcasWalkingEditorUpdater (WalkingEditorUpdater):
	"""
	recursively visits an entire directory structure and update all the .xml
	files it finds
	"""
		
	UPDATER_CLASS = UcasEditorUpdater
				
			
def showUsernameMappings():
	for key in usernameMappings.keys():
		print "%s: %s" % (key, usernameMappings[key])

if __name__ == "__main__":
	# baseDir = os.path.join (UCAS_DIR, 'records/dcs_data')
	##baseDir = os.path.join (UCAS_DIR, 'records/dcs_data/library_dc/theses')
	baseDir = "test_collection"
	UcasWalkingEditorUpdater (baseDir)
	

