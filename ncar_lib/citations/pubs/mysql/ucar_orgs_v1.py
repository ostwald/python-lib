"""
UCAR organization info - extract information from the People/organization table of the form
	full_name (acronym)
	
	we have to distinguish between active and inactive organizations, and clean
	up the acronym and full_name values accordingly
	
"""
import sys, os
from UserDict import UserDict
from PeopleDB import PeopleDB, OrganizationRec

class OrgNode:
	"""
	wraps OrganizationRec to allow for a linked node (tree) structure
	"""
	
	def __init__ (self, orgRec, orgTable):
		self.orgRec = orgRec
		self.level = self._intOrNone(self.orgRec.org_level_id)
		self.id = self._intOrNone(self.orgRec.org_id)
		self.parent = self._intOrNone(self.orgRec.parent_org_id)
		self.active = self._intOrNone(self.orgRec.active) == 1
		
	def _intOrNone (self, val):
		try:
			return int(val)
		except:
			return -1
		
	def __repr__ (self):
		return "%d %s - active: %s, level: %d, parent: %d" % (self.id, self.orgRec.__repr__(), 
					self.active, self.level, self.parent)
					
class OrgTable(UserDict):
	def __init__ (self):
		UserDict.__init__ (self)
		db = PeopleDB()
		for orgRec in db.getOrganizations():
			if orgRec.full_name:
				orgNode = OrgNode (orgRec, self)
				self[orgNode.id] = orgNode
			
	def __getitem__ (self, key):
		if self.data.has_key(key):
			return self.data[key]
		else:
			return None
				
	def getLabs (self):
		return filter (lambda org: org.level == 4, self.values())
			
	def getSubDivisions (self):
		return filter (lambda org: org.level == 9, self.values())
		
	def getDivisions (self):
		return filter (lambda org: org.level == 1, self.values())
		
	def report(self):
		for id in self.keys():
			print "%s: %s" % (id, self[id])
			
	def getVocab (self, id):
		pp = []
		ptr = self[id]
		print ptr, '\n'
		
		# cut off when we reach UCAR, NCAR, BOARD or MEMBERS
		while ptr:
			pp.insert(0,"%s (%d)" % (str(ptr.orgRec), ptr.level))
			ptr = self[ptr.parent]
		return ':'.join (pp)
		
	def getLineage (self, id):
		"""
		ancestors starting from top and including self[id]
		"""
		lineage = []
		node = self[id]
		while node and node.level not in [3, 10, 8, 6]:
			lineage.append(node.id)
			node = self[node.parent]
		return lineage
		
	def getAncestors (self, id):
		ancestors = self.getLineage(id)
		ancestors.reverse()
		return ancestors
		
	def hierVocab (self, id):
		for i, id in enumerate(self.getAncestors(id)):
			print "%s%s (%d)" % (' '*i, self[id].orgRec, self[id].level)
		
	def fooberry (self, orgs):
		orgs = orgs or self.values()
		for org in orgs:
			print "\n%s (%d)\n%s" % (org.orgRec, org.level, '-'*len(str(org.orgRec)))
			self.hierVocab(org.id)
			
			
if __name__ == '__main__':
	orgTable = OrgTable()
	# orgTable.report()
	# print orgTable.getVocab(171)
	# print orgTable.hierVocab(171)
	# for org in orgTable.values():
		# print orgTable.ppRec(org.id)
	# orgTable.fooberry(orgTable.getLabs())
	# orgTable.fooberry(orgTable.getSubDivisions())
	orgTable.fooberry(orgTable.getDivisions())

