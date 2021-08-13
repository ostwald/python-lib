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
    print ("REFRESH")
    pp (resp.json())
    session = resp.json()['session']
    set_session (session)
    return session

def get_archival_object_data (obj_id):
    """
    see https://archivesspace.github.io/archivesspace/api/#get-an-archival-object-by-id
    :param obj_id: e.g., archival_object/22578
    :return: json response from ArchivesSpace API
    """
    url = os.path.join (ASPACE_API_BASE_URL, 'repositories/2', obj_id)
    return get_api_resp(url)

def get_api_resp(url, params=None):
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
        print ('ERROR in resp_json')
        pp (resp_json)
        if 'code' in resp_json and resp_json['code'] == "SESSION_GONE":
            print ('refreshing token')
            headers = {
                'X-ArchivesSpace-Session' : refresh_session_token()
            }
            resp = requests.get (url, headers=headers)
            resp_json = resp.json()
        else:
            raise Exception ("Aspace API Error: {}".format(resp_json['error']))
    return resp.json()

def get_children (obj_id):
    """

    :param obj_id: e.g., archival_object/22578
    :return: json response from ArchivesSpace API
    """
    url = os.path.join (ASPACE_API_BASE_URL, 'repositories/2', obj_id, 'children')
    return get_api_resp(url)


if __name__ == '__main__':
    # config = get_config()
    # print (config)
    # get_session_token()
    # config = get_config()
    # print (config)

    # session = get_session()
    # print ("session: ", session)

    id = 'archival_objects/22578' # has children
    # id = 'archival_objects/2294' # has ark
    # id = 'resources/67' # has ark but not good example?
    # id = 'digital_objects/813' # digital object

    obj = get_archival_object_data(id)
    # obj = get_children(id)
    pp (obj)
    if 1: #write obj to disk
        path = '/Users/ostwald/tmp/{}.json'.format(id.replace ('/','_'))
        fp = open(path, 'w')
        fp.write (json.dumps(obj, indent=2))
        fp.close()
        print ('wrote to', path)