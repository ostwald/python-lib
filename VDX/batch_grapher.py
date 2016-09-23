"""
Batch Grapher -
For each Instance:
- create a graph for all groups, as well as one for all the cards
- write these graphs to a directory named for the teacher/section
	${graph_repo}/teacher/section/group .vdx
"""
import os, sys
from VDX import getEcoServiceGraphData, LayoutVdxRecord
from VDX.bio.ecoServiceData import EcoServiceClient, DataTable, RosterTable

GRAPH_REPO = '/Users/ostwald/Documents/Work/CCS/CCS BIO/Relation-Graphs'

class InstanceGrapher:
	 
	def __init__ (self, teacher, section):
		self.teacher = teacher
		self.section = section

		# how do we find out what the sections are??
		eco_client = self.getEcoServiceClient()
		self.data_table = DataTable(eco_client.data)
		self.roster_table = RosterTable(eco_client.roster)
		self.groups = self.getGroups()
		
	def getEcoServiceClient(self):
		params = {
			'teacher' : self.teacher,
			'section' : self.section,
			'command' : 'data',
			'data_type' : 'all'
		}
		return EcoServiceClient(params)
		
	def getGroups (self):
		groups = [];add=groups.append
		seen_emails = [];seen=seen_emails.append
		for row in self.data_table:
			email = row['Creator']
			if email in seen_emails:
				continue
			user = self.roster_table.get(email);
			if not user:
				continue
			group = user['Group']
			if not group in groups:
				add(group)
			seen(email)
		return groups

	def processGraph (self, group=None, callback=None):
		params = {
			'teacher' : self.teacher,
			'section' : self.section,
		}
		if group is not None:
			params['group'] = group
			
		graphData = getEcoServiceGraphData(params)
		vdx = LayoutVdxRecord(graphData)
		# vdx.showEdgeData()
		print "teacher: %s \n- section: %s\n- group: %s" % (
				params['teacher'], 
				params['section'], 
				params.has_key('group') and params['group'] or '')
		
		print "%d shapes, %s edges" % (len(vdx.shapes.keys()), len(vdx.edges.keys()))
	
		if callback:
			callback(group, vdx)
	
	def batchProcess (self):
		for group in self.groups:
			self.processGraph(group, self.writeGraph)
		
		# graph all nodes
		// self.processGraph(None, self.writeGraph)
	
	def writeGraph (self, group, vdx):
		
		filename = '%s_%s_group_%s.vdx' % (self.teacher, self.section, group)
		
		sectiondir = os.path.join (GRAPH_REPO, self.teacher, self.section)
		if not os.path.exists(sectiondir):
			os.makedirs(sectiondir)
			
		path = os.path.join (sectiondir, filename)
		
		# out = out_graph_debug
		vdx.write(path)
		print 'wrote to', path

	
if __name__ == '__main__':
	ig = InstanceGrapher('brown', 'Period 2')
	# ig = InstanceGrapher('crump', 'Period 3')
	print 'ig.dataTable has %d items' % len(ig.data_table)
	print 'ig.dataTable has %d groups' % len(ig.groups)
	ig.batchProcess()
