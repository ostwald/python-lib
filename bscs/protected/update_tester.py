"""
Collection tester
"""
import os, sys, re, time, shutil
from bscs.protected import *
from url_rewriting_records import urlRewritingRecordClasses

def tester (collectionPath):
	collection = os.path.basename(collectionPath)
	xmlFormat = os.path.basename(os.path.dirname(collectionPath));
	
	for filename in filter(lambda x:x.endswith('.xml'), os.listdir(collectionPath)):
		path = os.path.join(collectionPath, filename)
		rec = urlRewritingRecordClasses[xmlFormat](path=path, collection=collection) 
		for url in rec.getProtectedUrls():
			verify(url, collection)
		
def verify(url, collection):                               
	assetPath = getAssetPath (url)

	newProtectedCollPath = os.path.join (getReorgProtectedDir(), collection)
	newAssetPath = os.path.join (newProtectedCollPath, os.path.basename(assetPath))
	newProtectedUrl = os.path.join (base_protected_url, collection, os.path.basename(assetPath))

	if not os.path.exists(assetPath):
		print 'assetPath not found for', assetPath
	if 0:
		print '\n- assetPath:', assetPath
		print '- newAssetPath:', newAssetPath
		print '- oldUrl:', url
		print '- newProtectedUrl:', newProtectedUrl

	
if __name__ == '__main__':
	collectionPath = '/Users/ostwald/devel/dcs-repos/reorg-workspace/dcs-reorg/records/dlese_anno/comment_bscs'
	recordsPath = '/Users/ostwald/tmp/untitled folder/records/'
	collectionPath = os.path.join (recordsPath, 'dlese_anno/comment_bscs')
	tester(collectionPath)
	
