"""
UCAR organization info - extract information from the People/organization table of the form
	full_name (acronym)
	
	we have to distinguish between active and inactive organizations, and clean
	up the acronym and full_name values accordingly
	
"""
import sys, os
from UserDict import UserDict
from PeopleDB import PeopleDB, OrganizationRec
from JloXml import XmlRecord, XmlUtils

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
		self.children = []
		self.ancestors = []
		
	def _intOrNone (self, val):
		try:
			return int(val)
		except:
			return -1
			
	def addChild (self, id):
		if not id in self.children:
			self.children.append(id)
		
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
			
		for org in self.values():
			parent = org.parent
			if parent > 0:
				parentNode = self[org.parent]
				if parentNode is None:
					print "parent node not found (id:%d)" % org.parent
				else:
					self[org.parent].addChild (org.id)
			org.ancestors = self._get_ancestors(org.id)
			# print "ancestors for %d: %s" % (org.id, org.ancestors)
				
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
		
	def _get_lineage (self, id):
		"""
		ancestors starting from top and including self[id]
		"""
		lineage = []
		node = self[id]
		# cut off when we reach UCAR, NCAR, BOARD or MEMBERS
		while node and node.level not in [3, 10, 8, 6]:
			lineage.append(node.id)
			node = self[node.parent]
		# print "linage for %d: %s" % (id, lineage)
		return lineage
		
	def _get_ancestors (self, id):
		ancestors = self._get_lineage(id)
		ancestors.reverse()
		# print "ancestors for %d: %s" % (id, ancestors)
		return ancestors
		
	def hierVocab (self, id):
		org = self[id]
		for i, id in enumerate(org.ancestors):
			node = self[id]
			print "%s%s (%d)" % (' '*i, node.orgRec, node.level)
		
	def fooberry (self, orgs, label=None):
		if label:
			print '\n%s\n%s' % (label, '-'*len(label))
		orgs = orgs or self.values()
		for org in orgs:
			if 0: # fancy and verbose
				print "\n%s (%d)\n%s" % (org.orgRec, org.level, '-'*len(str(org.orgRec)))
				# self.hierVocab(org.id)
			else:
				print "%s" % (org.orgRec)

	def asXml (self):
		rec = XmlRecord(xml="<orgchart/>")
		root = rec.doc
		for org in self.values():
			orgNode = rec.addElement (root, "node")
			orgNode.setAttribute ("id", str(org.id))
			# print "children: %s" % org.children
			children = XmlUtils.addElement (rec.dom, orgNode, "children")
			for child in org.children:
				# print "child: ", child
				XmlUtils.addChild(rec.dom, "child", str(child), children)
			XmlUtils.addChild(rec.dom, "parent", str(org.parent), orgNode)
			for attr in ['acronym', 'full_name', 'active', 'org_level_id']:
				val = getattr (org.orgRec, attr)
				XmlUtils.addChild (rec.dom, attr, str(val), orgNode)
			
		# print root.toxml()
		return rec
			
			

			
if __name__ == '__main__':
	orgTable = OrgTable()
	rec = orgTable.asXml()
	print rec
	
	# orgTable.report()
	# print orgTable.getVocab(171)
	# orgTable.hierVocab(171)
	# for org in orgTable.values():
		# print orgTable.ppRec(org.id)
	# orgTable.fooberry(orgTable.getLabs(), 'Labs')
	# orgTable.fooberry(orgTable.getSubDivisions(), 'SubDivisions')
	# orgTable.fooberry(orgTable.getDivisions(), 'Divisions')

