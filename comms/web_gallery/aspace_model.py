"""
MOdel the objects returned by the ArchivesSpace API
"""
import os, sys, json
from collections import UserDict
import aspace_api_client

class AspaceApiObject (UserDict):

    top_level_attrs = []

    def __init__ (self, data={}):
        self.data = data
        for attr in self.top_level_attrs:
            setattr (self, attr, data[attr])

class Note (AspaceApiObject):

    top_level_attrs = [
        'publish',
        'type',
        'subnotes',
    ]

    def __init__ (self, data):
        AspaceApiObject.__init__(self, data)

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
        self.rel_path = self.data['uri'].replace('/repositories/2/','')
        self._notes_map = None # map from type to note
        self.description = self.get_description()
        self.location = self.get_location()
        self.date = self.data['dates'][0]['begin']
        self._children = None

    def get_notes_map(self):
        if self._notes_map is None:
            self._notes_map = {}
            for note in map (Note, self.notes):
                self._notes_map[note.type] = note
        return self._notes_map

    def get_children(self):
        if self._children is None:
            self._children = list (map (ArchivalObject, aspace_api_client.get_children(self.rel_path)))
        return self._children

    def get_description (self):
        note = self.get_notes_map()['scopecontent']
        return note.subnotes[0]['content']

    def get_location (self):
        note = self.get_notes_map()['originalsloc']
        return ','.join (map (lambda x:x['content'], note.subnotes))

    def __repr__(self):
        s = '\n' + self.data['uri']
        for attr in ['level','jsonmodel_type', 'title', 'description', 'location', 'date']:
            s += '\n- ' + attr + ': ' + getattr(self, attr)
        return s

if __name__ == '__main__':
    # id = 'archival_objects/22563'
    id = 'archival_objects/22578'  # has children
    path = '/Users/ostwald/tmp/{}.json'.format(id.replace('/','_'))
    s = open(path, 'r').read()
    json_data = json.loads(s)
    obj = ArchivalObject(json_data)
    print ('read object:', obj['uri'])
    print (obj)
    children = obj.get_children()
    print (len(children), 'children')

    # aspace_api_client.pp (children[0].data)
    for p in children:
        print (p)