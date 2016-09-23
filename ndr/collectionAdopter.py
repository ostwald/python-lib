"""
collectionAdopter - we have a directory containing xml files of the following structuure:
	
	ndrMetadataInfo
		ndrHandle
		nsdl_dc
			nsdl_dc:nsdl_dc (this is the root of the nsdl_dc record)
		ncs_item
			record (this is the root of the ncs_item recorc)
			
for each record we want to:
	1 - generate a record ID
	2 - create a ncs_item record
		- set recordID
		- save to recordID+'.xml'
	3 - create a dcs_data Record
		- start with a template
		- set recordID
		- set ndrHandle
		- is there any other info this record needs?
		- save to recordID+'.xml'
"""
import os, sys, time, math
from JloXml import XmlRecord, XmlUtils, DcsDataRecord
from ncs import NcsItemRecord

local = "mgr"

if local == "mgr":
	outdir = "c:/tmp/CollectionAdopter/records_mgr"
	collection = '1228333818803' ## mgr
elif local == "localhost":
	outdir = "c:/tmp/CollectionAdopter/records_localhost"
	collection = '1235063028189' ## localhost

xmlformat = "ncs_item"

class CollectionAdopter (XmlRecord):

	xpath_delimiter = "/"
	dcs_data_template_path = "C:/tmp/dcsDataRecord-template.xml"
	prefix = "PRI"
	
	dowrite = 1

	def __init__ (self, path):
		XmlRecord.__init__ (self, path=path)
		self.id = self._make_id ()
		self.filename = self.id+".xml"
		self.timeStamp = self._get_time_stamp()
		self.ndrHandle = self.getTextAtPath ("ndrMetadataInfo/ndrHandle")
		
		self.ncs_item = self._make_ncs_item ()
		# print self.ncs_item
		
		self.dcs_data = self._make_dcs_data_record()
		# print self.dcs_data
		
	def _make_ncs_item(self):
		ncs_item_element = self.selectSingleNode (self.dom, "ndrMetadataInfo/ncs_item/record")
		if not ncs_item_element:
			raise Exception, "ncs_item element not found in %s" % self.path
		ncs_item = NcsItemRecord (ncs_item_element.toxml())
		ncs_item.setId (self.id)
		return ncs_item
		
	def _make_dcs_data_record (self):
		"""
		do not set last sync date!
		"""
		dcs_data = DcsDataRecord (path=self.dcs_data_template_path)
		dcs_data.setId (self.id)
		dcs_data.setNdrHandle (self.ndrHandle)
		
		dcs_data.addStatusEntry (status="Done", statusNote="Loaded from NDR", 
			editor="Unknown", changeDate=self.timeStamp)
		current_status = dcs_data.getCurrentStatusEntry()
		dcs_data.setLastTouchDate (self.timeStamp)
		dcs_data.setLastEditor ("Unknown")
		return dcs_data
		
	def _make_id (self):
		recnum = os.path.splitext(os.path.basename(self.path))[0]
		
		ones_fl, thous_fl = math.modf(float(recnum)/1000)
		ones = int (ones_fl*1000)
		thous = int(thous_fl)

		return "%s-000-000-%03d-%03d" % (self.prefix, thous, ones)
		
	def _get_time_stamp (self, time_tuple=None):
		if not time_tuple:
			time_tuple = time.localtime()
		timestamp_fmt = "%Y-%m-%dT%H:%M:%SZ"
		return time.strftime(timestamp_fmt, time_tuple)
		
	def write (self):
		item_dir = os.path.join (outdir, xmlformat, collection)
		if not os.path.exists(item_dir):
			os.makedirs (item_dir)
			
		dcs_data_dir = os.path.join (outdir, "dcs_data", xmlformat, collection)
		if not os.path.exists(dcs_data_dir):
			os.makedirs (dcs_data_dir)
			
		
		item_path = os.path.join (item_dir, self.filename)
		if self.dowrite:
			self.ncs_item.write (item_path)
			print 'wrote to ', item_path
		else:
			print 'WOULD have written to ', item_path
			
		dcs_data_path = os.path.join (dcs_data_dir, self.filename)
		if self.dowrite:
			self.dcs_data.write (dcs_data_path)
			print 'wrote to ', dcs_data_path
		else:
			print 'WOULD have written to ', dcs_data_path
		
def tester():
	path = "C:/tmp/CollectionAdopter/238.xml"
	ca = CollectionAdopter (path)
	print ca.ndrHandle
	print ca.id
	ca.write()		
	
if __name__ == "__main__":
	datadir = "C:/tmp/CollectionAdopter/ndrMetadataInfoRecords";
	for filename in os.listdir (datadir):
		if not filename.endswith (".xml"): continue
		path = os.path.join (datadir, filename)
		ca = CollectionAdopter (path)
		ca.write()	

		
		
