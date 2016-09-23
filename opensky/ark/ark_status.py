import sys, requests, re, logging
from lxml import etree

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
given an ark
- create an ark_url (http://n2t.net/ARK_ID)
- do a get on the url
	if status == 404 -> raise UNKNOWN ARK
	if status == 200 and r.url begins with http://ezid.cdlib.org/id -> RESERVED_ARK (return 0)
	if status == 200 and r.url begins with https://opensky.ucar.edu/islandora/object - ACTIVATED but need to verify
		grab pid from r.url and open fedora object and get obj_ark_id. 
		if obj_ark_id != ark_id ==> raise MISMATCH_ARK
		else
		  ==> ACTIVATED_ARK return 1
"""
class ArkException (Exception):
	pass
		
opensky_url_pat = re.compile ('(http|https)://opensky.ucar.edu/islandora/object')
		
def get_ark_status(ark):
	ark_url = "http://n2t.net/%s" % ark
	logging.debug ( 'ark_url %s' % ark_url)
	r = requests.get(ark_url)
	logging.debug ( 'status_code: %s' % r.status_code)
	logging.debug ( 'history %s' % r.history)
	logging.debug ( 'url %s' % r.url)
	
	if r.status_code == 404:
		raise ArkException, 'Unknown ark (%s)' % ark
	
	if r.url.startswith ("http://ezid.cdlib.org"):
		# RESERVED
		return 0
		
	if opensky_url_pat.match(r.url):
	   	   
		pid = r.url.split('/')[-1]
		logging.debug ( "pid: " + pid)
		obj_ark = get_obj_ark(pid)
		logging.debug ( 'obj_ark: %s' % obj_ark )
		if obj_ark == ark:
			# ACTIVATED
			return 1
		else:
			raise ArkException, 'Mismatched ARK (%s) - see %s' % (ark, pid)

	else:
		return ''
	raise ArkException, 'Ark did not resolve (%s)' % ark

def get_obj_ark(pid):
    r = requests.get ("http://osstage2.ucar.edu:8080/fedora/objects/{}/datastreams/MODS/content".format(pid))
    
    try :
        parser = etree.XMLParser(recover=True,encoding='utf-8')
        document = etree.fromstring(r.text.encode('utf-8'),parser)
        
        ns = {'m': 'http://www.loc.gov/mods/v3' }

        ark  = document.xpath('//m:identifier[@type="ark"]/text()', namespaces=ns)
        if len(ark) > 1:  
            pass # there is a problem here - claim it
        
        return ''.join(ark)
    except:
        return None 

def tester (ark):
	try:
		print get_ark_status (ark)
	except:
		print sys.exc_info()[1]

                
if __name__ == "__main__" : 
	tester('ark:/85065/d75q4t1t')


