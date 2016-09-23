from config_utils import *
from JloXml import DcsDataRecord

"""

	private final static String FINAL_STATUS_VALUE_TEMPLATE = "_|-final--|_";
	private final static Pattern FINAL_STATUS_PATTERN = Pattern.compile("_\\|-final-([^\\s]+)-\\|_");

	public final static String getFinalStatusValue(String collection) {
		return FindAndReplace.replace(FINAL_STATUS_VALUE_TEMPLATE, "--", "-" + collection + "-", false);
	}
	
"""


class DcsDataDir (ConfigDir):
	configClass = DcsDataRecord
	
	def getKey (self, rec):
		return rec.getId()
		
	def fixall (self):
		for rec in self.values():
			recFixer ( rec )
			
		
def recFixer (rec):

	fix_namespace(rec, dcs_data_namespace, dcs_data_schemaURI)
		
	status_list = rec.get_sortedEntryList()
	if status_list:
		entry = status_list[0]
		status = getattr (entry, "status")
		print "status: " + status

		
if __name__ == "__main__":
	path = "dcs_data"
	fcd = DcsDataDir (path)
	fcd.fixall()
	#fcd.report()
