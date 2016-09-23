"""
ark_reporter

for a collection an entry for each object:
pid, status, error
"""

import sys, logging, time
from opensky.ark.keiths_tools import get_collection_members, get_identifier_metadata
from opensky.ark.ark_status import get_ark_status, ArkException
from UserList import UserList
import requests, re
from lxml import etree

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def get_dil_metadata(pid):
    
    accession_num, dil_id, ark = "",'',''
    
    r = requests.get ("http://osstage2.ucar.edu:8080/fedora/objects/{}/datastreams/MODS/content".format(pid))
    
    try :
        parser = etree.XMLParser(recover=True,encoding='utf-8')
        document = etree.fromstring(r.text.encode('utf-8'),parser)
        
        ns = {'m': 'http://www.loc.gov/mods/v3' }
             
        accession_num = document.xpath('//m:identifier[@type="DIL-ACCESSION-ID"]/text()',namespaces=ns)
        dil_id     = document.xpath('//m:identifier[@type="DIL-FILE-ID"]/text()',namespaces=ns)
        ark     = document.xpath('//m:identifier[@type="ark"]/text()',namespaces=ns)
        
        if len(accession_num) > 1 or len(ark) > 1 or len(dil_id) > 1 : 
			print "HEY"
			pass # there is a problem here - claim it
        
        return ''.join(accession_num), ''.join(ark),  ''.join(dil_id)
    except :
        return None, None, None

class Extractor (UserList):
	
	MAX_PIDS = 1
	
	def __init__ (self, collection, fo_name=None):
		self.fo_name = fo_name or 'EXTRACTOR_OUT.csv'
		self.data = []
		self.collection = collection
		ticks = time.time()
		
		self.process()
		self.elapsed = time.time() - ticks
		
	def process(self):
		pid_num = 0
		with open(self.fo_name,"ab") as fo : 
			for pid in get_collection_members(self.collection):
				# print ('- %s'% pid)
				pid_num = pid_num + 1
				acc_num, ark, dil_id =  get_dil_metadata(pid)
				if acc_num is not None and ark is not None and dil_id is not None:
					line = ','.join([acc_num,ark,dil_id,pid])
					print '%d - %s' % (pid_num, line)
					fo.write(line + '\n')
					
				if pid_num >= self.MAX_PIDS:
					break
				
if __name__ == '__main__':
	collection = "opensky:imagegallery"
	rpt = Extractor(collection)

