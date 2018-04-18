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

if __name__ == '__main__':

    path = 'search_response.json'

    s = open(path, 'r').read()

    resp = SearchResponse(json.loads(s))

    for result in resp.results:
        print '\n'
        print result.title
        print '(%s)' % result.resource_type
        print '\n\t', result.summary





