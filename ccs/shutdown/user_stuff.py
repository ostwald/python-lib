import os, sys, re
# from user_content_searcher import DleseAnnoRecord, UserContentResult
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import MetaDataRecord, XmlUtils
from model import *

ddswsBaseUrlForUserContent = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"
purgBaseUrlForUserContent = "http://localhost:8070/dds/services/ddsws1-1"
ccsDevDDS = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"
prodDDS = "http://localhost:7248/dds/services/ddsws1-1"

class UserStuffResult (SearchResult):

    """
    Dynamically instantantiates result payload based on tagName (see get_payload_contructor)
    """
    default_payload_constructor = XmlRecord

    def __init__ (self, element, payload_constructor=None):
        SearchResult.__init__ (self, element, payload_constructor)


    def get_payload (self):
        metadata = self.selectSingleNode (self.dom, "record:metadata")
        children = XmlUtils.getChildElements(metadata)
        if not children:
            raise Exception, "Could not find payload"
        if len(children) != 1:
            raise Exception, "Found multiple payload elements"
        # print 'payload tag:', children[0].tagName
        constructor_class = self.get_payload_contructor(children[0].tagName)
        return  constructor_class (xml=children[0].toxml())

    def get_payload_contructor (self, tagName):
        switcher = {
            'playList' : PlaylistRecord,
            'savedResource' : SavedResource,
            'itemRecord' : AdnRecord,
        }
        default = XmlRecord
        return switcher.get(tagName, default)


class UserStuffSearcher (RepositorySearcher):

    default_baseUrl = prodDDS
    searchResult_constructor = UserStuffResult

    verbose=False
    numToFetch=10000

    def __init__ (self, userId, recordId=None):
        self.userId = userId
        self.recordId = recordId
        collection = 'ccsprivateannos'
        xmlFormat = 'dlese_anno'
        if recordId:
            self.filter_predicate = self.recordId_filter
        RepositorySearcher.__init__ (self, collection=collection, xmlFormat=xmlFormat, baseUrl=self.default_baseUrl)
    # print self.service_client.request.getUrl()

    def get_params(self, collection, xmlFormat):

        query = '/relation.isAnnotatedBy//key//annotationRecord/moreInfo/userSelection/@selectedByUserId:"%s"' % self.userId

        print 'query: %s' % query
        return {
            'q' : query,
            "verb": "Search",
            # "xmlFormat": xmlFormat,
            # "ky": collection,
            'relation' : 'isAnnotatedBy'
        }

    def recordId_filter (self, result):
        """
        keep only records that ha
        """
        selectPath = 'record:relations:relation:record:metadata:annotationRecord:moreInfo:userSelection:originalRecordId'
        originalRecordId = result.getTextAtPath(selectPath)
        # print ' filtering on ', originalRecordId
        return originalRecordId == self.recordId

if __name__ == '__main__':
    userId = '1247065132457'
    resources = UserStuffSearcher(userId)

    print '{} resources found for {}'.format(len(resources), userId)