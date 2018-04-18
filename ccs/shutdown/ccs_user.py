import os, sys, re
from lxml import etree as ET
from model import UserRecord, PlaylistRecord
from search_infrastructure import SearchResult, ResponseDoc, getResponse
from playlist_searcher import PlaylistSearcher


class UserSearchResult (SearchResult):
    payload_constructor = UserRecord

class UserResponseDoc (ResponseDoc):
    searchresult_constructor = UserSearchResult

def get_user (uuid):
    """
    User records are stored in dds, which is only available via tunnel
    :param uuid:
    :return:
    """
    params = {
        'verb' : 'Search',
        's' : '0',
        'n' : '10',
        'client' : 'devel',
        'ky' : 'ccsusers', # CCS: Users
        'q' : 'id:{}'.format(uuid)
    }

    baseurl = 'http://localhost:7248/dds/services/ddsws1-1'
    responseDoc = getResponse(baseurl, params, UserResponseDoc)
    return responseDoc.get_single_result_payload()

def get_user_playlists(userId):
    """
    searcher results are playlist results (payload is playlist record)
    :param userId:
    :return:
    """
    searcher = PlaylistSearcher(userId)
    print 'found {} playlists'.format(len(searcher.data))
    return map (PlaylistRecord, map (lambda x:str(x.payload), searcher))


def get_user_tester(userId):
    rec = get_user(userId)
    print rec
    id = rec.get_id()
    print 'User: {}, {} ({})'.format(rec.get_last_name(), rec.get_first_name(), rec.get_id())

if __name__ == '__main__':
    userId = '1247065132457'
    if 1:
        get_user_tester (userId)
    elif 1:
        results = get_user_playlists(userId)
        for pl in results:
            print '-', pl
        # print results[0]
        #
        # ids = map (lambda x:x.recId, results)
        # for recId in ids:
        #     print '-', recId