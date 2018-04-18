import os, sys, re
from lxml import etree as ET
from xml_record import XmlRecord
# from search_infrastructure import remove_namespace
from io import StringIO

class NoNamespaceRecord (XmlRecord):
    """
    Assumes all xpaths are of same (default) namespace
    Note: self.namespaces must be defined with "ddsws" being the
    default namespace
    """

    # override  me!!
    namespaces = {'ddsws' : 'http://www.dlese.org/Metadata/ddsws'}
    nspat = re.compile ('\/([A-Za-z0-9])')


    def selectNodesAtPath(self, path, context=None):
        """
        paths come in with no namespaces, we add namespace to all
        elements (but not attributes)

        this allows us to use paths without namespaces
        """

        def replfn (matchobj):
            """
            return the replacement value (inserting namespace)
            """
            return '/ddsws:{}'.format(matchobj.group(1))

        # account for not-attribute relative path
        if path[0] != '@' and path[0] != '/':
            path = 'ddsws:' + path

        ns_path = re.sub(self.nspat, replfn, path)
        # print 'ns_path: ', ns_path
        return XmlRecord.selectNodesAtPath(self, ns_path, context)

    def get_property(self, propname):
        path = '/java/object/void[@property="{}"]/string'.format(propname)
        return self.getTextAtPath(path)

class UserRecord (NoNamespaceRecord):

    # metadata_path =

    xpaths = {
        'id' : '/java/object/void[@property="userId"]/string',
    }
    namespaces = {'ddsws' : 'http://www.dlese.org/Metadata/ddsws'}

    def get_id (self):
        return self.get_property('userId')

    def get_first_name(self):
        return self.get_property('firstName')

    def get_last_name(self):
        return self.get_property('lastName')

    def get_email (self):
        return self.get_property('email')

    def summary (self):
        return 'User: {}, {} ({})'.format(self.get_last_name(), self.get_first_name(), self.get_id())

class PlaylistRecord (NoNamespaceRecord):

    xpaths = {
        'id' : '/playList/recordID',
        'title' : '/playList/title',
        'userID' : '/playList/userID',
        'description' : '/playList/description',
    }

    def __init__ (self, xml):
        NoNamespaceRecord.__init__ (self, xml)

        # fix for xmlns trash in items node (xlt namespace-out didn't do it)
        raw = ET.tostring(self.dom)
        self.dom = ET.fromstring (raw.replace ('xmlns=""', ''))

        for key in self.xpaths:
            setattr(self, key, self.getValueAtNamedPath(key))

    def summary (self):
        return 'Playlist: {} ({})'.format(self.title, self.id)

class AdnRecord (NoNamespaceRecord):

    namespaces = {
        'ddsws' : 'http://adn.dlese.org'
    }

    xpaths = {
        'id' : '/itemRecord/metaMetadata/catalogEntries/catalog/@entry',
        'title' : '/itemRecord/general/title',
        'description' : '/itemRecord/general/description',
        'url' : '/itemRecord/technical/online/primaryURL',
        'ccs_info_raw' : '/itemRecord/metaMetadata/description',
    }

    def __init__ (self, xml):
        NoNamespaceRecord.__init__ (self, xml)
        for key in self.xpaths.keys():
            setattr(self, key, self.getValueAtNamedPath(key))
        self.ccs_info = self._parse_ccs_info()

    def _parse_ccs_info(self):
        dict = {}
        lines = filter (None, map (lambda x:x.strip(), self.ccs_info_raw.split('\n')))
        for line in lines:
            if line[0] == '#':
                continue
            splits = map (lambda x:x.strip(), line.split('='))
            if len(splits) != 2:
                continue
            dict[splits[0]] = splits[1]
        return dict


    def summary (self):
        return 'AdnRecord: {} ({})\n\t{}'.format(self.title, self.url, self.ccs_info)



class SavedResource (XmlRecord):

    xpaths = {
        'id' : '/savedResource/id',
        'title' : '/savedResource/title',
        'savedXmlFormat' : '/playList/savedXmlFormat',
        'description' : '/playList/description',
        'savedRecordId' : '/savedResource/savedRecordId',
    }

    def __init__ (self, xml):
        XmlRecord.__init__ (self, xml)
        for key in self.xpaths.keys():
            setattr(self, key, self.getValueAtNamedPath(key))

    def get_savedRecord (self):
        """
        we don't know the tagName of the savedRecord so we just return
        the first (and only) child of the record tagset
        :return: Element
        """
        node = self.selectSingleNode ('/savedResource/record')
        if node is not None:
            # print ET.tostring(node[0], pretty_print=True)
            return node[0]


    def summary (self):
        return 'SavedResource: {} ({})'.format(self.title, self.id)