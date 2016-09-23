"""
see - https://docs.google.com/document/d/1QuaGgyYhS-OMjCG3Y8YaE7jK6XoSOZK6_EnQm_JLvcA/edit
"""
import requests, re
from lxml import etree

def get_identifier_metadata(pid):
    
    osid, ezid, nldr_url = "",'',''
    
    r = requests.get ("http://osstage2.ucar.edu:8080/fedora/objects/{}/datastreams/MODS/content".format(pid))
    
    try :
        parser = etree.XMLParser(recover=True,encoding='utf-8')
        document = etree.fromstring(r.text.encode('utf-8'),parser)
        
        ns = {'m': 'http://www.loc.gov/mods/v3' }
             
        nldr_url = document.xpath('//m:identifier[@type="uri" and @displayLabel="Legacy citable URL"]/text()',namespaces=ns)
        osid     = document.xpath('//m:recordIdentifier[@source="CoBA"]/text()',namespaces=ns)
        ezid     = document.xpath('//m:identifier[@type="ark"]/text()',namespaces=ns)
        
        if len(nldr_url) > 1 or len(ezid) > 1 or len(osid) > 1 :  
            pass # there is a problem here - claim it
        
        return ''.join(nldr_url), ''.join(ezid),  ''.join(osid)
    except :
        return None, None, None

def get_collection_members(collection_root = "archives:vinlally"):
    payload = \
        { 'type'   : 'tuples',
          'format' : 'csv',
          'lang'   : 'itql',
          'query'  : 'select $object from <#ri> where  $object <fedora-rels-ext:isMemberOfCollection> <info:fedora/{}>'.format(collection_root)
        }
        
    r = requests.get("http://osstage2.ucar.edu:8080/fedora/risearch",params=payload)
    
    # result will come back like info:fedora/archives:1999
    for d in r.text.split("\n"):
        if "/" in d :  
            yield d.split('/')[1]  


def main():
    
    fo_name = "../../../production/identifiers/archives_ezid_pid_production_map_test.csv"
    collections = ['archives:hao','archives:vinlally','archives:mesalab','archives:nhre','archives:unid']
        
    with open(fo_name,"ab") as fo :         
        for c in collections : 
            for pid in get_collection_members(c):        
                n, e, o =  get_identifier_metadata(pid)
                if n is not None and e is not None and o is not None:
                    fo.write("{}|{}|{}|{}\n".format(o,e,pid,n))

                
if __name__ == "__main__" : main()

