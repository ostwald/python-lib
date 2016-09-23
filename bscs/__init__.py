""" 
The bscs package supports the task of merging BSCS repositories
(Curriculum and UserContent) into the respective CSS repositories.

Detecting ID conflicts across two repositories - this package takes the following
approach. First the IDs defined in the repository are obtained via DDSWebservice
and written to disk in files named for collecitions (and holding the IDs for that
collection). Then, the IDs are read and compared for unique IDs by another set of
tools.

Tools to download a Repo's Ids and userInfo via DDS webservice. The IDs are cached
on disk in a top-level directory named for the repo (e.g., id_cache/CCS0 and then
in a file named to reflect ids, e.g., "userIds.txt", "playlistIds.txt").

- getIds.py - obtain Ids using webservices, and write data to disk 

- getUserInfo.py - obtain userInfo using webservices, and write data to disk 

Tools to find duplicateIDs in the cached IDa

- dataSet.py - reads data file from disk into lists of Ids. dataSet subclasses
  read from multiple files (e.g., all the files in repo, or just files for collections
  where the IDs are system-generated).

- idSet.py - a collection of ids - supplied by a dataSet. IdSets can compare 
  against another IdSet, finding missing and/or duplicate Ids.

- userInfoSet.py - like IdSet, but can also compare usernames

Tools to manipulate records and find userSaves
(these require a file-system access to repository)

- collection_tool.py -  change the key and prefix of a collection.

- assign_statuses.py - traverse the dcs_data tree and assign a done status to all records.

- user_saves.py - finds the userSaves (annos in ccsprivateannos).

Tools that actually do the merge(s)
(also assume repositories accessible on disk)

- curriculum_merge.py - copies all item-level curriculum metadata collections
  from bscs to ccs. Collisions raise exceptions in write mode.
  
- user_content_merger - merge BSCS collections into their (existing) respective
  collections. Preparation includes looking for username collisions.

"""
import sys, re, os
host = os.environ['HOST']

class RepoInfo:
	def __init__ (self, name, baseUrl):
		self.name = name
		self.baseUrl = baseUrl 
		
# primary BSCS Repositories

bscs_curriculum = RepoInfo("BSCS_Curriculum", "http://localhost:7148/dcs/services/ddsws1-1")
bscs_user_content = RepoInfo("BSCS_User_Content", "http://localhost:7148/dds/services/ddsws1-1")

# CCS Repositories - production server - requires tunneling
if host == 'purg.local':
	ccs_merged_curriculum = RepoInfo("CCS_Merged_Curriculum", "http://localhost:8070/curricula/services/ddsws1-1")
	ccs_merged_user_content = RepoInfo("CCS_Merged_User_Content", "http://localhost:8070/dds/services/ddsws1-1")

elif host == 'acornvm':
	ccs_merged_curriculum = RepoInfo("CCS_Merged_Curriculum", "http://ccs-test.dls.ucar.edu/schemedit/services/ddsws1-1")
	ccs_merged_user_content = RepoInfo("CCS_Merged_User_Content", "http://http://acornvm.dls.ucar.edu:17248/dds/services/ddsws1-1")
elif host == 'DLS-pyramid':
	ccs_merged_curriculum = RepoInfo("CCS_Merged_Curriculum", "http://localhost:8080/schemedit/services/ddsws1-1")
	ccs_merged_user_content = RepoInfo("CCS_Merged_User_Content", "http://localhost:8080/dds/services/ddsws1-1")
else:
	raise Exception, "Unknown host: %s" % host
class UserInfo:
	def __init__ (self, name, id):
		self.name = name
		self.id = id

# users that have potential name/id conflicts
bscs_ccs_dup_users = [
	UserInfo ('Loretta', '1309470489284'),
	UserInfo ('chall', '1332132886692'),
	UserInfo ('cruiz', '1369405477255'),
	UserInfo ('holly', '1307937315411'),
	UserInfo ('jweather', 'ADMIN'),
	UserInfo ('mmassimo', '1339440516888'),
	UserInfo ('ostwald', '1311287237585'),
	UserInfo ('tammy', '1309470489285'),
]
	
