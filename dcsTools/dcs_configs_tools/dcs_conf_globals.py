import os
"""
globals related to the dcs_conf directories for various DCS instances
"""

collection_config_schemaURI = "http://www.dlese.org/Metadata/dcs/collection-config/dcsCollectionConfig.xsd"
collection_config_namespace = "http://dcs.dlese.org/collection-config"

framework_config_schemaURI = "http://www.dlese.org/Metadata/dcs/framework-config/dcsFrameworkConfig.xsd"
framework_config_namespace = "http://dcs.dlese.org/framework-config"

dcs_data_schemaURI = "http://www.dlese.org/Metadata/dcs/dcs-data/dcs-data.xsd"
dcs_data_namespace = "http://dcs.dlese.org/dcs-data"

dcs_conf_dir_map = {
	'DLS-SanLuis' : 'C:/Program Files/Apache Software Foundation/Tomcat 5.5/var/dcs_conf',
	'mast' : '/dls/devweb/imls.dls.ucar.edu/tomcat/dcs_conf',
}

def getConfigDir (key=None):
	key = key or os.getenv('HOST')
	try:
		return dcs_conf_dir_map[key]
	except:
		raise Exception, 'dcs_conf not found for ' + key
		
def getFrameworksDir (key=None):
	return os.path.join (getConfigDir (key), "frameworks")
	
def getCollectionsDir (key=None):
	return os.path.join (getConfigDir (key), "collections")
	
