import os, sys, re

from serviceclient import SimpleClient, SimpleClientError
from lxml import etree as ET
from xml_record import XmlRecord
from model import NoNamespaceRecord

class SearchResult (NoNamespaceRecord):

    payload_constructor = XmlRecord
    namespaces = {'ddsws' : 'http://www.dlese.org/Metadata/ddsws'}
    xpaths = {
        'head' : "/ddsws:record/ddsws:head",
        'id' : "/ddsws:record/ddsws:head/ddsws:id",
        'ky' : "/ddsws:record/ddsws:head/ddsws:collection[@ky]",
        'metadata' : "/ddsws:record/ddsws:metadata",
    }

    #
    def __init__ (self, xml):
        XmlRecord.__init__(self, xml)
        for key in self.xpaths:
            setattr(self, key, self.getValueAtNamedPath(key))

    def get_payload (self):
        metadata = self.selectNodeAtNamedPath("metadata")
        return self.payload_constructor(ET.tostring(metadata[0]))

class ResponseDoc (XmlRecord):
    namespaces = {'ddsws' : 'http://www.dlese.org/Metadata/ddsws'}
    searchresult_constructor = SearchResult

    def __init__(self, xml):
        XmlRecord.__init__(self, xml)
        result_elements = self.selectNodesAtPath("/ddsws:DDSWebService/ddsws:Search/ddsws:results/ddsws:record")

        self.results = map (self.searchresult_constructor, map (lambda x:ET.tostring(x), result_elements))

    def get_single_result_payload (self):
        """
        the payload is the first element of the first metadata
        """

        if len(self.results) != 1:
            raise Exception, 'Expected one record, got {}'.format(len(results))

        return self.results[0].get_payload()

def getResponse (baseUrl, params, responseDoc_class=ResponseDoc):
    client = SimpleClient (baseUrl)
    xml = client.getData(params=params)
    lines = xml.split('\n')
    if lines[0].find ('<?xml') > -1:
        lines = lines[1:]
    xml = '\n'.join(lines).strip()

    return responseDoc_class(xml)

def apply_transform (dom, xls_path, verbose=0):
    """
    :param dom: TREE to be transformed
    :param xls_path: path to transform
    :return:
    """
    if verbose :
        print 'APPLY_TRANSFORM: %s' % xls_path

    xsl_doc = ET.parse(xls_path)
    xform = ET.XSLT(xsl_doc)
    return xform(dom)

def remove_namespace(dom):
    return apply_transform(dom, '/Users/ostwald/devel/python-lib/ccs/namespace-out.xsl')

if __name__ == '__main__':
    path = '/Users/ostwald/tmp/savedResource.xml'
    doc = ET.parse(path)
    foo = remove_namespace(doc)
    print ET.tostring(foo)