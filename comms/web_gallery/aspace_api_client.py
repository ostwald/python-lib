import sys, os, re, traceback
import json
import requests

# ASPACE_API_BASE_URL = 'http://osws-p.ucar.edu:7089'
ASPACE_API_BASE_URL = 'https://aspace-p-api.ucar.edu'
CONFIG_PATH = 'config.json'

def pp (obj):
    print (json.dumps(obj, indent=2))

def get_config ():
    return json.loads (open (CONFIG_PATH, 'r').read())

def update_config(config):
    fp = open(CONFIG_PATH, 'w')
    fp.write(json.dumps (config, indent=2))
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
    config['session'] = session
    update_config(config)
    return config

def get_object (obj_path):
    url = os.path.join (ASPACE_API_BASE_URL, 'repositories/2', obj_path)
    return get_api_resp(url)

def get_api_resp(url, params=None):
    config = get_config()
    headers = {
        'X-ArchivesSpace-Session' : config['session']
    }
    resp = requests.get (url, headers=headers, params=params)
    resp_json = resp.json()
    if 'error' in resp_json:
        print ('ERROR in resp_json')
        # pp (resp_json)
        if 'code' in resp_json and resp_json['code'] == "SESSION_GONE":
            print ('refreshing token')
            config = refresh_session_token()
            headers = {
                'X-ArchivesSpace-Session' : config['session']
            }
            resp = requests.get (url, headers=headers)
            resp_json = resp.json()
        else:
            raise Exception ("Aspace API Error: {}".format(resp_json['error']))
    return resp.json()

def get_children (obj_path):
    url = os.path.join (ASPACE_API_BASE_URL, 'repositories/2', obj_path, 'children')
    return get_api_resp(url)


if __name__ == '__main__':
    # config = get_config()
    # print (config)
    # get_session_token()
    # config = get_config()
    # print (config)
    id = 'archival_objects/22578'
    obj = get_object(id)
    # obj = get_children('archival_objects/22578')
    pp (obj)
    if 0: #write obj to disk
        path = '/Users/ostwald/tmp/{}.json'.format(id.replace ('/','_'))
        fp = open(path, 'w')
        fp.write (json.dumps(obj, indent=2))
        fp.close()
        print ('wrote to', path)