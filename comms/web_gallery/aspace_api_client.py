"""
interact with the ArchivesSpace API
- https://archivesspace.github.io/archivesspace/api/
"""
import sys, os, re, traceback
from web_gallery import get_config, update_config
import json
import requests



# ASPACE_API_BASE_URL = 'http://osws-t2-api.dls.ucar.edu'
# ASPACE_API_BASE_URL = 'https://aspace-p-api.ucar.edu'

# ASPACE_API_BASE_URL = 'http://osws-p.ucar.edu:7089' # works
# ASPACE_API_BASE_URL = 'http://libdev2.cloud.ucar.edu:7089' # works
# CONFIG_PATH = 'config.json'
# TOKEN_PATH = '_session_token'
# CONFIG_PATH = 'config.json'


CONFIG = get_config()
ASPACE_API_BASE_URL = CONFIG['aspace_api_base_url']
TOKEN_PATH = CONFIG['session_token_path']

def pp (obj):
    print (json.dumps(obj, indent=2))

def get_session():
    if os.path.exists(TOKEN_PATH):
        return open(TOKEN_PATH, 'r').read().strip()
    return None

def set_session(token):
    fp = open(TOKEN_PATH, 'w')
    fp.write(token)
    fp.close()

def refresh_session_token ():
    config = get_config()
    params = {'password':config['password']}
    url = os.path.join (ASPACE_API_BASE_URL,
                        'users/{}/login'.format(config['user']))
    resp = requests.post (url, params)
    # print ("REFRESH")
    # pp (resp.json())
    session = resp.json()['session']
    set_session (session)
    return session

def get_archival_object_data (obj_uri):
    """
    see https://archivesspace.github.io/archivesspace/api/#get-an-archival-object-by-id
    :param obj_id: e.g., archival_object/22578
    :return: json response from ArchivesSpace API
    """
    if not obj_uri.startswith ("/repositories/2/"):
        if 1:
            print ("BAD ARG")
        obj_uri = "/repositories/2/" + obj_uri
    url = os.path.join (ASPACE_API_BASE_URL + obj_uri)
    return get_api_resp(url)

def get_digital_objects ():
    """
    see https://archivesspace.github.io/archivesspace/api/#get-an-archival-object-by-id
    :param obj_id: e.g., archival_object/22578
    :return: json response from ArchivesSpace API
    """
    url = os.path.join (ASPACE_API_BASE_URL, 'repositories/2/digital_objects')
    return get_api_resp(url, {
        'page' : 1,
        'page_size' : 15
    })

def post_api_resp(url, params, data=None):
    config = get_config()
    headers = {
        # 'X-ArchivesSpace-Session' : config['session']
        'X-ArchivesSpace-Session' : get_session()
    }
    resp = requests.post (url, headers=headers, params=params, data=data)
    return resp.json()

def search_resp(params):
    """
    params include query
    :param url:
    :param params:
    :return: list of search result json objects
    """
    query_params = {
        'q' : '*',
        'page' : '1',
        'utf' : 'true',
        'page_size' : '10'
    }
    query_params.update(params)
    url = CONFIG['aspace_api_base_url']+'/repositories/2/search'
    resp = get_api_resp(url, params=params)
    return resp['results']

def get_locations_records (path=None):
    """
    primary_type:archival_object AND notes:"originalsloc CIC-ExternalDisk1/disc1/alex_guenther"
    :return:
    """
    debug = False
    query = "primary_type:archival_object AND "
    if path is None:
        query +=  'notes:"originalsloc CIC-ExternalDisk1"'
    else:
        query += 'notes:"originalsloc {}"'.format(path)

    print ("query: ", query)

    params = {
        'q' : query,
        'page' : '1',
        'utf' : 'true',
        'page_size' : '60'
    }

    return search_resp(params)

def get_api_resp(url, params=None):
    """
    submits a get api request
    :param url:
    :param params:
    :return:
    """
    debug = False
    config = get_config()
    headers = {
        # 'X-ArchivesSpace-Session' : config['session']
        'X-ArchivesSpace-Session' : get_session()
    }
    resp = requests.get (url, headers=headers, params=params)
    resp_json = resp.json()
    # print (url)
    # pp (resp_json)
    if 'error' in resp_json:
        if debug:
            print ('ERROR in resp_json')
            pp (resp_json)
        if 'code' in resp_json and resp_json['code'] == "SESSION_GONE":
            if debug:
                print ('refreshing token')
            headers = {
                'X-ArchivesSpace-Session' : refresh_session_token()
            }
            resp = requests.get (url, headers=headers)
            resp_json = resp.json()
        else:
            raise Exception ("Aspace API Error: {}".format(resp_json['error']))
    return resp.json()

def get_children (obj_uri):
    """

    :param obj_id: e.g., archival_object/22578
    :return: json response from ArchivesSpace API
    """
    url = os.path.join (ASPACE_API_BASE_URL + obj_uri, 'children')
    return get_api_resp(url)


if __name__ == '__main__':
    # config = get_config()
    # print (config)
    # get_session_token()
    # config = get_config()
    # print (config)

    # session = get_session()
    # print ("session: ", session)

    notes = "323a2f5530e20d1ec704804b8374ecc1 originalsloc CIC-ExternalDisk1/disc1/alex_guenther"
    path_pat = re.compile (".*originalsloc ([^\s]*).*")
    m = path_pat.match(notes)
    if m:
        print ('match: "{}"'.format(m.group(1)))
    if 0:  # get location records
        path = '/CIC-ExternalDisk1/disc2/craig_blurton'
        path = None
        records = get_locations_records(path)
        print (len(records), " found with path: {}".format(path))

        rec = records[0]
        pp (rec)
        pp (rec['notes'])

    if 0: # get an archival object
        # id = 'archival_objects/22578' # has children
        id = 'archival_objects/16841' # has digital object as instance
        # id = 'archival_objects/2294' # has ark
        # id = 'resources/67' # has ark but not good example?
        # id = 'digital_objects/897' # digital object
        obj = get_archival_object_data('/repositories/2/{}'.format(id))
        # obj = get_children(id)
        pp (obj)
    if 0:
        id = 'digital_objects/897' # digital object
        obj = get_archival_object_data('repositories/2'+id)
        # obj = get_children(id)
        pp (obj)

    if 0: #write obj to disk
        path = '/Users/ostwald/tmp/{}.json'.format(id.replace ('/','_'))
        fp = open(path, 'w')
        fp.write (json.dumps(obj, indent=2))
        fp.close()
        print ('wrote to', path)

    if 0:
        resp = get_digital_objects()
        print (json.dumps(resp, indent=2))