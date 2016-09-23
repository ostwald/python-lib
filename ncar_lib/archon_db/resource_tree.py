"""
Resource Tree

For some given root node (e.g., a collection record, a resource)

1 - read in all resources
2 - create parent map
3 - start with root (parent = 0)
4 - depth first on each:
  - get all resources with parent = current id
    - calculate

"""
import os, sys, time, re
from UserDict import UserDict

class ResourceNode:
	
	def __init__ (self, rec):
		self.parent = rec['ParentID']
		self.children = []
		self.rec = rec

class ResourceTree (UserDict):
	
	report_depth = 10
	
	def __init__ (self, resources):
		self.data = {}
		map (self.add, resources)
			
	def add (self, resource):
		parent = str(int(resource['ParentID']))
		parent_nodes = self.data.has_key(parent) and self[parent] or []
		parent_nodes.append(resource)
		self[parent] = parent_nodes
	
	def node_cmp(self, node1, node2):
		return cmp(node1['SortOrder'], node2['SortOrder'])
			
	def report (self, root='0', level=0):
		if level == 0:
			self.des_found = 0
		if level > self.report_depth:
			return
		root = str(int(root))
		if not self.has_key(root):
			return
		children = self[root]
		children.sort (cmp=self.node_cmp)
		indent = level*'  '
		for node in children:
			asterisk = ''
			if node['Description'] is not None:
				self.des_found += 1
				asterisk = '*'
				
			# print '%s- %d - %s' % (indent, level, node['Title'])
			# print '%s- %s, %s (%s)' % (indent, node['Title'], node['Date'], node['SortOrder'])
			print '%s- %s, %s (%s)%s' % (indent, node['Title'], node['Date'], node['ID'], asterisk)

			# print '%s- %s, %s' % (indent, node['Title'], node['Date'])
			self.report (node['ID'], level+1)
			
		if level == 0: # last out
			print "\n*%d description nodes found" % self.des_found
if __name__ == '__main__':
	from archon_collection import getCollection
	coll_id = 30
	schema = schema = ['ID','Title','Date','ParentID', 'SortOrder']
	collection = getCollection(coll_id)
	recs = collection.items
	
	print '%d recs for %s' % (len(recs), collection.title)
	
	tree = ResourceTree (recs)
	tree.report(root='0')
				
