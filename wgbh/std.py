from rpcclient import encode
from UserDict import UserDict



class StdNode:

	indent = "  "
	truncate = 100

	def __init__ (self, data, parent=None, level=0):

		self.ASN_id = encode(data['ASN_id'])
		self.description = encode(data['description'])
		self.children = UserDict()
		self.level = level
		for child in data['children']:
			node = StdNode (child, self, self.level+1)
			self.children[node.ASN_id] = node

	def prtln (self, s):
		print '%s%s' % (self.level*self.indent, s)

	def report (self):
		description = self.description
		if len (description) > self.truncate:
			description = description[:self.truncate] + " ..."
		if self.level == 0:
			self.prtln ('%s' % (description))
		else:
			self.prtln ('%s (%s)' % (description, self.ASN_id))
		# self.prtln (self.ASN_id)
		for child in self.children.values():
			child.report()
			
class StdTree:
	
	def __init__ (self, data, jurisdiction):
		self.jurisdiction = jurisdiction
		self.root = StdNode (data)
		self.leaves = []
		self._get_leaves()
		
	def _get_leaves(self, node=None):
		node = node or self.root
		for id in node.children.keys():
			child = node.children[id]
			if not child.children:
				self.leaves.append (id)
			else:
				self._get_leaves (child)
		
	def report (self):
		print "\n%s standards hierarchy\n" % self.jurisdiction
		print "leaf nodes:"
		for l in self.leaves:
			print "\t", l
		self.root.report()
