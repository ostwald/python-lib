"""
MOdel the objects returned by the ArchivesSpace API
"""
import os, sys, json, re
from collections import UserDict
import aspace_api_client

def pp (obj):
    print (json.dumps(obj, indent=2))

class AspaceApiObject (UserDict):

    top_level_attrs = []

    def __init__ (self, data={}):
        self.data = data
        for attr in self.top_level_attrs:
            try:
                setattr (self, attr, data[attr])
            except:
                setattr(self, attr, None)

class Note (AspaceApiObject):

    top_level_attrs = [
        'publish',
        'type',
        'subnotes',
    ]

    def __init__ (self, data):
        AspaceApiObject.__init__(self, data)

class DigitalObject (AspaceApiObject):
    top_level_attrs = [
        'digital_object_id',
        'publish',
        'uri',
        'jsonmodel_type',
        'title',
        'notes'
    ]
    def __init__ (self, data):
        """
        data is the API response to get object
        :param data:
        """
        self.ark = None
        AspaceApiObject.__init__(self, data)
        try:
            self.ark = self.digital_object_id.replace('http://n2t.net/','')
        except:
            pass

class ArchivalObject (AspaceApiObject):
    """
    Encapsulate the ArchivesSpace Object returned by the API
    see https://archivesspace.github.io/archivesspace/api/#get-an-archival-object-by-id

    to expose:
    - level (file | item)
    - title
    - description
    - date
    - children
    - jsonmodel_type (e.g., archive_object)
    - location - CIC-ExternalDisk1/disc2/awards2004
    - uri - /repositories/2/archival_objects/22578
    - id - e.g., archival_objects/22578
    """

    top_level_attrs = [
        'level',
        'uri',
        'jsonmodel_type',
        'title',
        'notes',
        'display_string'
    ]

    def __init__ (self, data):
        """
        data is the API response to get object
        :param data:
        """
        AspaceApiObject.__init__(self, data)
        # pp(data)
        self.rel_path = self.data['uri'].replace('/repositories/2/','')
        # self.uri = self.data['uri']
        self.parent_uri = self.data['parent']['ref']
        self.publish = self.data['publish']
        self._notes_map = None # map from type to note
        self.description = self.get_description()
        self.location = self.get_location()
        if len(self.data['dates']) > 0 and 'begin' in self.data['dates'][0]:
            self.date = self.data['dates'][0]['begin']
        else:
            self.date = ''
        self._children = None
        self._children_map = None

        if self.level == 'item':
            self.image_name = os.path.basename(self.location)
        else:
            self.image_name = ''

        self.creators = []
        for item in self.data['linked_agents']:
            if 'role' in item and item['role'] == 'creator':
                self.creators.append(item['ref'])

        self.creator = None
        if len(self.creators) > 0:
            self.creator = self.creators[0]  # usually there is only one creator, right?

    def get_notes_map(self):
        if self._notes_map is None:
            self._notes_map = {}
            for note in map (Note, self.notes):
                self._notes_map[note.type] = note
        return self._notes_map

    def get_children(self):
        """

        :return: a list of ArchivalObject instances
        """
        if self._children is None:
            self._children = list (map (ArchivalObject, aspace_api_client.get_children(self.uri)))
        return self._children

    def get_child(self, image_name):
        """

        :param image_name:
        :return: an ArchivalObject instance
        """
        if self._children_map is None:
            self._children_map = {}
            for child_object in self.get_children():
                image_name = child_object.image_name
                # print ('- {} - {}'.format(image_name, child_object.rel_path))
                if image_name is None:
                    raise Exception ("child image_name is None for {}".format(child_object.rel_path))
                if image_name in self._children_map:
                    msg = "duplicate image_name: {} (see {})".format(image_name, child_object.rel_path)
                    # raise Exception (msg)
                    print ('WARN: {}'.format(msg))
                    continue
                self._children_map[image_name] = child_object
        if not image_name in self._children_map:
            return None
        return self._children_map[image_name]


    def get_description (self):
        try:
            note = self.get_notes_map()['scopecontent']
            return note.subnotes[0]['content']
        except:
            pass

    def get_location (self):
        """
        points to a relative location on disk where the digital object can be
        found on disk.
        :return:
        """
        try:
            note = self.get_notes_map()['originalsloc']
            return ','.join (map (lambda x:x['content'], note.subnotes))
        except:
            pass

    def get_digital_object_ref (self):
        """
        we look for an "instance that is a digital_object
        :return:
        """
        for instance in self.data['instances']:
            if instance['instance_type'] == "digital_object":
                return instance['digital_object']['ref']

    def add_digital_ark_object (self, ark):
        # the json for this object is self.data

        #     1 - create a digital object
        if 1: # create digital object from scratch
            dig_obj = {
                'title': self.data['display_string'],
                'digital_object_id' : ark,  # note: this is in clickable form in the archival object
                'file_versions':[{'file_uri':ark,
                                  'publish':True}],
            }
            params = {'repo_id': 2}
            url = os.path.join (aspace_api_client.ASPACE_API_BASE_URL, 'repositories/2/digital_objects')
            dig_obj_json = aspace_api_client.post_api_resp (url, params=params, data=json.dumps(dig_obj))

        if 0: # grab an existing digital object - we just crated this one using postman
            url = os.path.join (aspace_api_client.ASPACE_API_BASE_URL, 'repositories/2/digital_objects/894')
            dig_obj_json = aspace_api_client.get_api_resp (url)

        # print ("DIGITAL OBJ");
        # pp (dig_obj_json)

        dig_obj_uri = dig_obj_json['uri']
        # print ('dig_obj_uri:', dig_obj_uri)

        ## Now attach digital object to archival object as an "instance"
        archival_object_json = self.data

        # print ("ARCHIVAL OBJECT JSON")
        # pp (archival_object_json)

        dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}
        archival_object_json['instances'].append(dig_obj_instance)
        # archival_object_json['lock_version'] = archival_object_json['lock_version'] + 1
        url = aspace_api_client.ASPACE_API_BASE_URL+ self.uri
        # print ("URL: ", url)
        archival_object_update = aspace_api_client.post_api_resp (url, params=None, data=json.dumps(archival_object_json))

        ## Was update successful?
        print ("UPdated ARCHIVAL OBJECT")
        pp (archival_object_update)

        if 'error' in archival_object_update:
            raise Exception ("could not update archival object: {}".format(archival_object_update['error']))
    def __repr__(self):
        s = '\n' + self.data['uri']
        for attr in ['level','jsonmodel_type', 'title', 'description', 'location', 'date']:
            s += '\n- ' + attr + ': ' + getattr(self, attr)
        return s

def get_archival_object (archival_id):
    """

    :param archival_id: e.g., 'archival_objects/22578'
    :return:
    """
    try:
        return ArchivalObject(aspace_api_client.get_archival_object_data (archival_id))
    except Exception as err:
        raise Exception ("Could not get Archival objects for {}: {}".format(archival_id, err))


def get_digital_object (archival_id):
    """

    :param archival_id: e.g., 'archival_objects/22578'
    :return:
    """
    return DigitalObject(aspace_api_client.get_archival_object_data (archival_id))

def get_person_data (person_uri):
    try:
        int(person_uri)
        person_uri = '/agents/people/{}'.format(person_id)
    except:
        pass
    data = aspace_api_client.get_api_resp(aspace_api_client.ASPACE_API_BASE_URL + person_uri)
    # pp(data)
    return data

def get_person_name (person_uri):
    try:
        data = get_person_data(person_uri)
        return "{} {}".format(data['display_name']['rest_of_name'], data['display_name']['primary_name'])
    except:
        return None

class LocationMap (UserDict):
    """
    maps locations from ASpace (using uri) and file-based Web Galleries (using file path)

    ARKS stored in Aspace Objects will use the path to compute a targetURL.

    maps from uri to pathk and back from path to uri
    """
    path_pat = re.compile (".*originalsloc ([^\s]*).*")

    def __init__ (self, data_path=None):
        if data_path is None:
            self.initialize_from_aspace()
        else:
            self.data = json.loads(open(data_path, 'r').read())

        # initialize path_map
        self.path_map = {}

        for uri in self.data:
            self.path_map[self.data[uri]] = uri


    def initialize_from_aspace(self):
        self.data = {}
        location_records = aspace_api_client.get_locations_records()
        for rec in location_records:
            m = self.path_pat.match(rec['notes'])
            if m:
                self.data [rec['uri']] = m.group(1)
                # self.path_map[m.group(1)] = rec['uri']

    def get_path (self, uri):
        """

        :param uri: e.g., "/repositories/2/archival_objects/22576"
        :return: a path (e.g., CIC-ExternalDisk1/disc2/amik_st-cyr)
        """
        return self[uri]

    def get_uri (self, path):
        """
        :param path: e.g., CIC-ExternalDisk1/disc2/amik_st-cyr
        :return: uri (e.g., "/repositories/2/archival_objects/22576")
        """
        return self.path_map[path]

    def write (self, outpath="/Users/ostwald/tmp/LOCATOR.json"):
        fp = open(outpath, 'w')
        fp.write (json.dumps(self.data, indent=2))
        fp.close()
        print ("wrote to ", outpath)

if __name__ == '__main__':

    id = 'archival_objects/22563'  # test
    # id = 'archival_objects/22578'  # production has children

    if 0:  # LOCATION MAP
        data_path = '/Users/ostwald/tmp/LOCATOR.json'
        locator = LocationMap(data_path)
        print (len(locator), 'locations mapped')
        if 0:
            uri = '/repositories/2/archival_objects/22576'
            path = locator.get_path(uri)
        else:
            path = 'CIC-ExternalDisk1/disc2/15-25-35-2005/print'
            uri = locator.get_uri(path)
        print ('path: ', path)
        print ('uri: ', uri)
        # locator.write()

    if 0:
        path = '/Users/ostwald/tmp/{}.json'.format(id.replace('/','_'))
        s = open(path, 'r').read()
        json_data = json.loads(s)
        obj = ArchivalObject(json_data)
    if 1:
        uri = '/repositories/2/archival_objects/22653'
        ark = 'ark:/85065/d7hx1h0p'
        obj = get_archival_object(uri)
        pp(obj.data)

        if 0: # digital object stuff
            dobj_uri = obj.get_digital_object_ref()
            print ("digital object: {}".format(dobj_uri))

            if dobj_uri:
                dobj = get_digital_object(dobj_uri)
                print ("ark_link: " + dobj.digital_object_id)
                print ("ark: " + dobj.ark)

        if 0:
            obj.add_digital_ark_object('http://n2t.net/'+ark)



    if 0:
        children = obj.get_children()
        print (len(children), 'children')

        # aspace_api_client.pp (children[0].data)
        for p in children:
            print (p)