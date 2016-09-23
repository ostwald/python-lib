"""
tools for 
- checking User Content repositories for UserName collisions
  (aka dup_user), 
- configuring ths module to accomodate dup_users, and
- finding all the user-saves by dup-users

Finding dupUserNames
	1 - first we have to obtain userInfo from the both
	the BSCS and CCS userContent repositories via DDS webservice
	
	2 - then we can compare the userInfo to identify duplicate userNames
	- see user_info_set.userInfoReport()
	
	NOTE: If there are duplicate user names (and in the case of the BSCS there are):
	- collect the userName, userId pairs (from report), and 
	-  if necessary update bscs.bscs_ccs_dup_users (see __init__.py)

To find all user-saves by user run TallyUserSaves

Use these tools to record state before user_content_merge and then
after to verify.

"""
import os, sys, re, time
from bscs import bscs_user_content, ccs_merged_user_content
from getIds import cacheUserIds, getIds
from getUserInfo import cacheUserInfo, getUserInfo, reportDupUserNames
from user_info_set import userInfoReport, UserInfoSet

"""
the full-blown approach is to cache IDs to disk and then run
idset functions over pairs of data sets
"""

def connection_tester():
	"""
	this doesn't cached the ids but simply reports how many
	there are.
	"""
	for repoDDS in [bscs_user_content, ccs_merged_user_content]:
		collection = 'ccsusersubmittedresources'
		try:
			ids = getIds(repoDDS, collection=collection)
			print 'there are %d ids for %s' % (len(ids), collection)
		except Exception, msg:
			print "getIds ERROR with %s dds: %s" % (repoDDS.baseUrl, msg)

#verify user names

def refreshUserInfoCache ():
	for repoDDS in [bscs_user_content, ccs_merged_user_content]:
		cacheUserInfo (repoDDS)
		
if __name__ == '__main__':
	if 0:
		# are we communicating with the servers?
		connection_tester()
	
	# if we need to create or refresh id cache for userInfo	
	if 0:
		refreshUserInfoCache()
	
	if 1:
		# print out report of dup users
		userInfoReport() 
		
	
	if 0:
		# see how many records the dup users have saved
		from user_saves import TallyUserSaves
		TallyUserSaves(bscs_user_content)
	
	if 0:
		# AFTER merging - check ccs-merged for dups
		reportDupUserNames (ccs_merged_user_content)
