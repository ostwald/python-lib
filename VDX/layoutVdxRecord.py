"""
LayoutVdxRecord

gets EdgeData from an external source (see GraphData)

EdgeData looks like this:
{'targetLabel': None, 'source': u'1423249652449', 'sourceLabel': u'BearValley Coyote (7)', 'target': u'O2', 'relation': u'produces'}
{'targetLabel': None, 'source': u'1423249652527', 'sourceLabel': u'Berrian Elk2', 'target': u'1423249652379', 'relation': u'decomposes'}

gets Layout (which specifies node positions from graph defined by edges)

"""
import sys, os
# from bio import getEdgeData as getBioEdgeData
from bio import DATA_SERVICE_URLS
from bio import CvsGraphData, getEcoServiceGraphData
from JloGraph import Layout
from VDX import DrawVDX, VdxRecord, Circle, Rectangle, Line
from UserDict import UserDict
from colors import Colors
import util


class LayoutVdxRecord (VdxRecord):
	"""
	Extends VdxRecord to compute a graph layout (self.layout)
	
	layout args:
	- iterations - Number of FDL iterations to run in coordinate generation
    - force_strength - Strength of Coulomb and Hooke forces
                     (edit this to scale the distance between nodes)
    - dampening - Multiplier to reduce force applied to nodes
    - max_velocity - Maximum distance a node can move in one step
    - max_distance - The maximum distance considered for interactions
	
	"""
	verbose = 0
	origin = [5,5] # to place center near center of page
	layout_args = {
		'force_strength' : 2, #1.2, # determine spread - smaller number shorter edges
		'max_velocity' : 6.0, # doesn't seem to matter too much
		'iterations' : 5000,
		'max_distance' : 200 # default is 50 - 200 looks better, 2 is bad
	}
	
	def __init__(self, graphData):
		
		VdxRecord.__init__(self)
		self.graphData = graphData
		self.colors = Colors()
		# self.graphData = self.GraphDataImpl()
		"""
		up to the first 7 elements work, from then on the VDX cannot be imported!
		e.g., 
		# self.edgeData = self.graphData.getEdgeData()[:6] # works
		# self.edgeData = self.graphData.getEdgeData()[:7] # does NOT work
		"""
		# self.edgeData = self.graphData.getEdgeData()
		self.edgeData = self.graphData.getEdgeData()

		if len(self.edgeData) == 0:
			self.addEmptyGraphNode()
			return

		self.layout = Layout (self.edgeData, **self.layout_args)
		if self.verbose:
			print self.layout
	
		self.addNodes();
		
		self.addEdges();
		
	def _shapeGetter (self, shapeId):
		return self.getShapeByName(shapeId)
		
	def __repr__ (self):
		"""
		remove spaces so they won't be seen by Lucid,
		which for some reason does not ingore them
		"""
		return self.dom.toxml()
		
	def addEmptyGraphNode(self):
		main = {
			'name' : "main",
			'x' : 2,
			'y' : 8.5,
			'width' : 2.5,
			'height' : 2,
			'label': {
				'text': 'Empty Graph!',
				'color': '#0000ff',
				'size':32
			}
		}
		
		details = {
			'name' : "details",
			'x' : 1.5,
			'y' : 7.0,
			'width' : 3.5,
			'height' : .5,
			'label': {
				'text': 'There were no relations to show',
				'color': '#0000ff',
				'size':14
			}
		}			
		
		self.addNode(Circle, main)
		self.addNode(Rectangle, details)
		self.addEdge("main", "details", "details")
		
	def addNodes(self):
		"""
		use location from layout to create nodes (Shapes) and 
		insert them in this record
		"""
		
		def getName (id):
			return self.graphData.data_table.getNameFromId(id)
		
		# create the args that will define shapes in vdx
		for id, data in self.layout.nodes.iteritems():
			
			# print ' - %s: %s' % (id, getName(id))
			record = self.graphData.data_table.get(id)
			orgType = None
			if (record):
				orgType = record['OrganismType']

			if 0:
				print '-------'
				print ' - %s: %s (%s)' % (id, getName(id), orgType)
				print ' - text: %s' % self.colors.getColor(orgType,'text')
			
			pos = data['location']
			args = {
				'name': id, 
				'label': {
					'text':getName(id),
					'size':10,
					'color':self.colors.getColor(orgType,'text') or '#000000'
				},
				'line' : {
					'color':self.colors.getColor(orgType,'line') or '#000000'
				},
				# 'label': {'text':id},
				'x':pos[0] + self.origin[0],
				'y':pos[1] + self.origin[1], 	
				'width':1.0,
				'height':0.5,
				'color':'#2e62ff'
			}
			
			# print "adding shape at %s, %s" % (args['x'], args['y'])
			id = self.addNode(Circle, args)
			
			# sanity/debugging check
			shape = self.getShape(id)
			
			if not shape:
				# print vdx
				# print '-----------'
				# print 'shape keys:'
				# for key in vdx.shapes.keys():
					# print ' - %s (%s)' % (key, type(key))
				print "ERROR shape not found for added shape (%s) ... HALTING" % id
				sys.exit()
			if self.verbose:
				print ' ... (%s - %f, %f)' % (shape.Name, shape.PinX, shape.PinY)
			
	def makeEdgeShapeOFF (self, fromShape, toShape, relation, id):
		"""
		given two endpoints (the connectors) ...
		PinX is midpoint of x's
		PinY is midpoint of y's
		
		this function has to compute the input parameters to
		the Line constructor (to be implemented)
		
		XForm1D is inserted in Shape
		ObjectType = 2
		
		"""
		if self.verbose:
			print 'LayoutVDX - makeEdgeShape()'
		def avg (a, b):
			return (float(a) + float(b)) / 2.00000000
			
		def diff (a, b):
			return (float(a) - float(b))
		
		start = fromShape.getBestConnection(toShape)
		end = toShape.getBestConnection(fromShape)
		
		if self.verbose:
			print 'makeConnectorShape source=%s, target=%s' % (fromShape.ID, toShape.ID)
			print ' - start: %f, %f' % (start[0], start[1])
			print ' -   end: %f, %f' % (end[0], end[1])
		
		line_args = {
			'name': 'connector_%d' % (len(self.edges)+1),
			'label':{'text':relation, 'size':10},
			'x' : start[0],
			'y' : start[1],
			'height' : diff (end[1], start[1]) or util.pt2in(2),
			'width' : diff (end[0],start[0]),
			'begin_x' : start[0],
			'begin_y' : start[1],
			'end_x' : end[0],
			'end_y' : end[1]
		}
		
		# print 'line_args'
		# for k, v in line_args.iteritems():
			# print ' - %s: %s' % (k,v)
		
		return Line (id, line_args)

	def addEdges (self):
		"""
		create lines (Shapes) to represent the graph edges.
		insert the lines into the DOM
		
		NOTE: we are not making explicit connections at this time.
		they do not seem to be necessary, since the shapes when imported
		into lucid have connections anyway
		"""
		for data in self.layout.edges:

			source = data['source']
			target = data['target']
			
			if self.verbose:
				print 'source: %s target: %s'  % (source, target)
			self.addEdge (source, target, data['relation'])			
			

	def showEdgeData (self):
		print 'EdgeData (%d)' % len(self.edgeData)
		for item in self.edgeData:
			if 1:
				print item
			else:
				print ' - source: %s, target: %s, relation: %s' % \
					(item['source'], item['target'], item['relation'])

if __name__ == '__main__':
	if 0:
		teacher, section, group = 'crump', 'Period 3', '1' # works with SPRING_15
		baseUrl_name = 'SPRING_15'

	elif 0:
		teacher, section, group = 'crump', 'Period 3', '2' # works with
		baseUrl_name = 'FALL_15'
	else:
		teacher, section, group = 'brown', 'Periods 4 and 7', '1' # works with
		baseUrl_name = 'FALL_15'
		
	params = {
		'section' : section,
		'teacher' : teacher,
		'group' : group,
		# 'ecoSurvey
	}
	# baseUrl = 'https://script.google.com/macros/s/AKfycbxlWucHZ59oW6V9mjCS0VKwGwu4lIjuCEqd8AIVVFfCdjfe6buq/exec'
	baseUrl = DATA_SERVICE_URLS[baseUrl_name]
	graphData = getEcoServiceGraphData(params, baseUrl)
	# graphData = CvsGraphData()
	vdx = LayoutVdxRecord(graphData)
	vdx.showEdgeData()
	
	if 1:
		print "%d shapes, %s edges" % (len(vdx.shapes.keys()), len(vdx.edges.keys()))
		print vdx
	if 0:
		out = '/Users/ostwald/Desktop/VDX/%s_%s_%s.vdx' % (
				params['teacher'], params['section'], 
				params.has_key('group') and params['group'] or '')
		
		force_strength = vdx.layout_args['force_strength']
		max_velocity = vdx.layout_args['max_velocity']
		iterations = vdx.layout_args['iterations']
		max_distance = vdx.layout_args['max_distance']
		
		out_graph_debug = '/Users/ostwald/Desktop/VDX/strength_%s_iterations_%s_distance_%s.vdx' % (
				force_strength, iterations, max_distance)
		
		# out = out_graph_debug
		vdx.write(out)
		print 'wrote to', out
