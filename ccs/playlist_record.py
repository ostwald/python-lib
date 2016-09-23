"""
extract resources from playlist record
"""

import os, sys, re
from JloXml import XmlRecord, XmlUtils

def getResourceIds (path):
	rec = XmlRecord(path=path)
	item_nodes = rec.selectNodes(rec.dom, 'playList:items:item')
	# print '%d item_nodes found' % len(item_nodes)

	ids=[];add=ids.append
	for node in item_nodes:
		if node.getAttribute('type') == 'ccs_saved_resource':
			id_node = XmlUtils.getChild ('id', node)
			add (XmlUtils.getText(id_node))
	ids = filter (lambda x:not x.startswith('CCS'), ids)
	return ids

def getUserId (path):
	rec = XmlRecord(path=path)
	return rec.getTextAtPath('playList:userID')
	
if __name__ == '__main__':
	# path = "/Users/ostwald/tmp/playlist_move_2_26/playlist-2.xml" # playlist 2 from ccs_prod
	path = "/Users/ostwald/tmp/playlist_move_2_26/playlist-1.xml" # playlist 2 from ccs_prod
	# path = '/Users/ostwald/devel/dcs-repos/dds-ccs-dev/ccs_user_content/records_ccs_users/playlist/ccsplaylists/1356157556365.xml'
	ids = getResourceIds (path)
	print '\nRESOURCE IDs'
	for id in ids:
		print '- ',id
		
	print '\nUSER: %s' % 	getUserId(path)

