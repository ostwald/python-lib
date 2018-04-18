"""
tools to aid in shutdown of ccs, such as knowing what users have accessed system
and what they've uploaded

ME: 1247065132457

"""

import os, sys, re
from lxml import etree as ET
from xml_record import XmlRecord
from search_infrastructure import SearchResult, ResponseDoc
from model import PlaylistRecord, UserRecord, SavedResource, AdnRecord


