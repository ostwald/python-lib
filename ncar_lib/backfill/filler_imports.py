from ncar_lib.lib import globals, webcatUtils, accessionNumMappings, frameworks
from ncar_lib.lib.frameworks import LibraryDCRec

def drNum2RecId (drNum):
	return "TECH-NOTE-000-000-%3s-%3s" % (drNum[-6:-3],drNum[-3:])
	
