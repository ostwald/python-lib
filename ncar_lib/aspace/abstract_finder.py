
import requests
from UserDict import UserDict
from model import SearchResponse, SearchResult
import json

from ncar_lib.aspace.aspace_proxy import AspaceProxy

class MyProxy (AspaceProxy):

    pass

# def get_abstract(notes):
#     for note in notes:
#         note_type = note.get('type')
#         pid = note.get('persistent_id')
#         label = note.get('label')
#         print '- {} ({}) - {}'.format(label, note_type, pid)


def search_tester (proxy):
    # proxy = MyProxy()
    response = proxy.search("warren washington")

    for result in response.results:
        # print '\n'
        # print result.id
        # print result.title
        # print '(%s)' % result.resource_type
        # print '\n\t', result.summary
        pass

    result = response.results[0]

    abstract = result.get_abstract_note()

    print json.dumps(abstract, indent=3)

if __name__ == "__main__":
    MyProxy.baseurl = 'http://aspace-t.dls.ucar.edu:7089'
    proxy = MyProxy ('admin', 'tornado')
    # search_tester(proxy)
    id = '15661'
    archival_obj = proxy.get_archival_object(id)
    print archival_obj

