import os, sys, re
from lxml import etree as ET
from ccs_user import get_user
from ccs_activity.user_content_tester import UserContentTester, getSelectedUserResources
from user_stuff import UserStuffSearcher
from model import *

def user_report (userId):
    user = get_user(userId)

    print user.summary()

    user_stuff = UserStuffSearcher(userId)

    user_stuff.sort (key=lambda x:x.payload.__class__.__name__)

    for result in user_stuff:

        if 1 or isinstance(result.payload, AdnRecord):
            print '\n', result.recId, result.payload.summary()

            try:
                # if result.payload.ccs_info['recordId'] == '1386955317551':
                if 0 and result.recId == '1386955317551':
                    print result
                    fp = open ("/Users/ostwald/tmp/STUFF.xml", 'w')
                    fp.write(str(result))
            except:
                pass

        # if isinstance(result.payload, SavedResource):
        #     print '\n', result.payload.summary()
        #     print '\t',result.payload.get_savedRecord().tag

def playlist_report (playlistId):
    from playlist_searcher import ResourceSearcher
    playlist_result = None
    try:
        playlist_result = ResourceSearcher([playlistId,])[0]
        playlist_record = PlaylistRecord(unicode(playlist_result.payload))
    except:
        print 'ERROR: {}'.format(sys.exc_info()[1])
        return

    # print playlist_result


    print playlist_record.summary()

    # fp = open('/Users/ostwald/playlist.xml', 'w')
    # fp.write (ET.tostring(playlist_record.dom, pretty_print=1))
    resources = playlist_record.selectNodesAtPath("///item[@type='ccs_saved_resource']")

    print '{} resources found'.format(len(resources))

    for res in resources:

        id = playlist_record.getTextAtPath('id', res)
        print id

if __name__ == '__main__':
    # userId = '1247065132457'
    # user_report(userId)

    playlistId = '1373641283726'
    playlist_report(playlistId)

