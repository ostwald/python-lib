"""
EcoService Client
"""
import os, sys, time
import json
from JloGraph import Layout
from ecoServiceData import *

class CytoData:

	position_multiplier = 25

	def __init__ (self, teacher, section, group, baseUrl_name='FALL_15'):
		self.teacher = teacher
		self.section = section
		self.group = group
		self.baseUrl_name = baseUrl_name
		self.node_labels = {}
		try:
			self.layout = self._get_layout()
		except:
			print "ERROR: could not compute layout: %s" % sys.exc_info()[1]
			sys.exit()
		self.edges = self.getEdgeData() # edges must be computed first!

		self.nodes = self.getNodeData()


	def _get_layout(self):
		params = {
			'section' : self.section,
			'teacher' : self.teacher,
			'group' : self.group,
			'command' : 'data',
			'data_type' : 'all',
			'force' : 'true'
		}

		baseUrl = DATA_SERVICE_URLS[self.baseUrl_name]
		graphData = GraphData(params, baseUrl)
		edgeData = graphData.getEdgeData()
		print "%d Edges computed" % len(edgeData)

		return Layout(edgeData)


	def getEdgeData(self):
		"""
		as side effect, populate
		:return:
		"""

		self.node_labels = {}
		edges = []
		for edge in self.layout.edges:
			data = {'data': {
				'source': edge['source'],
				'target': edge['target'],
				'label': edge['relation'],
			}
			}
			self.node_labels[edge['data']['targetId']] = edge['data']['targetLabel']
			self.node_labels[edge['data']['sourceId']] = edge['data']['sourceLabel']
			edges.append(data)
		return edges

	def getNodeData(self):
		nodes = []

		for nodeId in self.layout.nodes:
			pos = self.layout.nodes[nodeId]['location']
			nodes.append(
					{
						'data': {
							'id': nodeId,
							'name': self.node_labels[nodeId]
						},
						'position': {
							'x': pos[0] * self.position_multiplier,
							'y': pos[1] * self.position_multiplier
						}
					}
			)
		return nodes

	def getCytoData(self):
		return { 'nodes' : self.nodes, 'edges': self.edges }

	def write_js_data(self, out="CYTO_DATA.js"):


		js_elements = "ELEMENTS = " + json.dumps (self.getCytoData(), indent=4, separators=(',', ': '))

		# print json.dumps (ELEMENTS, indent=4, separators=(',', ': '))

		fp = open(out, 'w')
		fp.write(js_elements)
		fp.close()
		print "wrote to %s" % out

	def write_json_data(self, out="CYTO_DATA.js"):
		fp = open(out, 'w')
		fp.write(json.dumps (self.getCytoData(), indent=4, separators=(',', ': ')))
		fp.close()
		print "wrote to %s" % out

def tester():
	teacher, section, group = 'brown', 'Periods 4 and 7', '2' # works with

	out = '/Users/ostwald/www/cyto/ELEMENTS.js'

	cytoData = CytoData(section=section, teacher=teacher, group=group)
	print '======================='
	# print json.dumps (cytoData.getCytoData(), indent=4, separators=(',', ': '))
	cytoData.write_js_data(out)


if __name__ == '__main__':
	teacher, section = 'brown', 'Periods 4 and 7'
	for group_num in range(1,11):
		filename = 'Group_%d.json' % group_num
		path = os.path.join('/Users/ostwald/www/cyto/data', filename)
		cytoData = CytoData(section=section, teacher=teacher, group=str(group_num))
		cytoData.write_json_data(path)

