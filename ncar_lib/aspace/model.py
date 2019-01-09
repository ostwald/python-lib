import os, sys, re
import json
from UserDict import UserDict

class SearchResponse (UserDict):

    def __init__ (self, data={}):
        self.data = data
        self.facets = self.data.get('facets')
        self.results = map(SearchResult, self.data.get('results'))

class SearchResult(UserDict):

    def __init__ (self, data={}):
        self.data = data
        self.id = self.get('id')
        self.title = self.get('title')
        self.level = self.get('level_enum_s')
        self.idenfier = self.get('identifier')
        # self.resource_type = self.get('resource_type_enum_s')
        self.primary_type = self.get('primary_type')
        self.resource_type = self.get('resource_type')
        self.publish = self.get('publish') == 'true'
        self.subjects = self.get('subjects')
        self.repository = self.get('repository')
        self.summary = self.get('summary')
        self.notes = self.get('notes')
        self.uri = self.get('uri')


        json_data = json.loads(self.get('json'))
        self.notes_json = json_data.get('notes')


    def get_abstract_note(self):
        for note in self.notes_json:
            note_type = note.get('type')
            pid = note.get('persistent_id')
            label = note.get('label')
            print '- {} ({}) - {}'.format(label, note_type, pid)
            if note_type == 'abstract':
                return note

class AspaceObject (UserDict):
    """
    encapsulate an Archival Object in Aspace
    """
    def __init__ (self, data):
        self.data = data

    def __repr__ (self):
        return json.dumps(self.data, indent=4)

class ArchivalObject (AspaceObject):
    """
    encapsulate an Archival Object in Aspace
    """

    def get_instance_OLD (self):
        """
        Assumes there is only ONE instance object
        Raise error otherwise
        :return:
        """
        instances = self.data['instances']
        if not len(instances) == 1:
            raise Exception, "ArchivalObject: %d Instances found" % len(instances)
        return instances[0]

    def get_instance (self):
        """
        There may be more than one instance for an ArchivalObject

        we look for an instance that has a top_container defined

        return
        :return: json Instance data or None if not found
        """
        instances = self.data['instances']
        if not len(instances):
            raise Exception, "ArchivalObject: No Instances found"
        for instance in instances:
            # print json.dumps(instance, indent=3)
            try:
                instance['sub_container']['top_container']
                return instance
            except:
                pass
        return None

    def get_top_container (self):
        instance = self.get_instance()
        return instance['sub_container']['top_container']['ref']

    def set_top_container (self, top_container_id):
        """
        Set the top_container to specified top_container_id.
        Assumes there should be a single top container only!
        :param tcid:
        :return:
        """
        instance = self.get_instance()
        instance['sub_container']['top_container']['ref'] = '/repositories/2/top_containers/%s' % top_container_id

class TopContainer (AspaceObject):
    pass

if __name__ == '__main__':
    from aspace_proxy import AspaceProxy

    class MyProxy (AspaceProxy):
        """
        used to obtain Objects from the API and to update objects via API
        """
        baseurl = 'http://aspace-t.dls.ucar.edu:7089'
        default_user = 'admin'
        default_passwd = 'tornado'

    proxy = MyProxy()
    id = '16253'
    obj = proxy.get_archival_object (id)
    instance = obj.get_instance()
    print instance






