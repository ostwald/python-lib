"""
python query builders to understand how to extract info relevant to activity stream

can we query for private annos created since 5/1/13??

"""
import os, sys, re
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import MetaDataRecord, XmlUtils

ddswsBaseUrlForCurricula = "http://acorn.dls.ucar.edu:27248/dcs/services/ddsws1-1"

ddswsBaseUrlForUserContent = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"


