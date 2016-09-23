import sys, os, re, copy
from JloXml import XmlRecord, XmlUtils, MetaDataRecord
from UserDict import UserDict
from shape import Circle, Rectangle
from line import Line
from connector import makeConnectorShape
import util

class VdxRecord (MetaDataRecord):
	verbose = 0
	xpath_delimiter = '/'
	# default_vdx_template = 'VDX-TEMPLATE.xml'
	default_vdx_template = util.getTemplate('VDX-TEMPLATE')
	
	def __init__ (self, template=None):
		template = template or self.default_vdx_template
		MetaDataRecord.__init__ (self, path=template)
		self.shapes = UserDict()
		self.edges = UserDict()
		self.nodes = UserDict()
	
	def getShapeNodes (self):
		"""
		return the shape elements from DOM
		"""
		return self.selectNodes (self.dom, 'VisioDocument/Pages/Page/Shapes/Shape')
	
	def getShapeId (self):
		
		return str(len(self.getShapeNodes())+1)
	
	def _shapeGetter (self, shapeId):
		return self.getShape(shapeId)
	
	def getShapeByName(self, name):
		# print 'getShapeByName (%s)' % name
		for node in self.shapes.values():
			if node.Name == name:
				return node
	
	def getShape(self, shapeId):
		"""
		return the Shape instance for provided shapeId or None if not defined
		"""
		return self.shapes.has_key(shapeId) and self.shapes[shapeId] or None
		
	def makeEdgeShape(self, source, target, relation, id=None):
		id = id or self.getShapeId()
		# return makeConnectorShape(source, target, relation, self.getShapeId())
		line_args = {
			'name': 'connector',
			'label':{'text':relation},
			# 'x' : avg (start[0], end[0]),
			# 'y' : avg (start[1], end[1]),
			# 'x' : start[0],
			# 'y' : start[1],
			# 'height' : diff (end[1], start[1]) or util.pt2in(2),
			# 'width' : diff (end[0],start[0]),
			# 'begin_x' : start[0],
			# 'begin_y' : start[1],
			# 'end_x' : end[0],
			# 'end_y' : end[1]
		}
		return Line (id, line_args)
		
	def addEdge(self, sourceId, targetId, relation):
		try:
			# source = self.getShape(sourceId)
			#source = self.getShapeByName(sourceId)
			source = self._shapeGetter(sourceId)
			if not source:
				raise Exception, "sourceId '%s'" % sourceId
			# target = self.getShape(targetId)
			# target = self.getShapeByName(targetId)
			target = self._shapeGetter(targetId)
			if not target:
				raise Exception, "targetId '%s'" % targetId
		except Exception, msg:
			print "addEdge Error: could not find a shape (%s)" % msg
			# print self
			print "SHAPE KEYS: %s" % self.shapes.keys()
			for key in self.shapes.keys():
				# print "%s: %s" % (key, self.shapes[key])
				print " - ",key
			print "HALTInG ..."
			sys.exit()
			
		# edge = makeConnectorShape(source, target, relation, self.getShapeId())
		edge = self.makeEdgeShape(source, target, relation, self.getShapeId())
		
		# parent = self.selectSingleNode (self.dom, 'VisioDocument/Pages/Page/Shapes')
		# if not parent:
			# raise xml.dom.NotFoundErr, 'Shapes node not found'
		# parent.appendChild(edge.getElement());
		
		self.edges[edge.ID] = edge
		self.addShapeObj (edge)
		
		# add the connect element
		self.addConnect (edge, source, target)
		
		return edge.ID
		
	# def addNode (self, id, constructor, args):
		# shape = klass(id, args)
		# self.addShapeObj(shape)
		# return id
		
	def addConnect(self, edge, source, target):
		"""
		create the LOGICAL connection between source and target
		- edge - the PHYSICAL connection (the line) is edge
		- source, target - ids, not objects
		
		This is an OBJECT-based connects, which connects the line
		to the objects as a whole rather than to a connection point on the object.
		
		OBJECT-based connects are supported	by draw.io
		"""
		# connects = self.selectSingleNode (self.dom, 'VisioDocument/Pages/Page/Connects')
		# if not connects:
			# raise Exception, 'CONNECTs element not found in VDX'
		parent = self.selectSingleNode (self.dom, 'VisioDocument/Pages/Page')
		if not parent:
				raise Exception, 'Page element not found in VDX'
		
		# create the Connects element, which specifies the
		# LOGICAL connection
		# 1 - connect edge/line to source
		connects = self.addElement (parent, 'Connects')
		connect1 = self.addElement(connects, 'Connect')	
		connect1.setAttribute ('FromSheet', edge.ID)
		connect1.setAttribute ('FromPart', '9')
		connect1.setAttribute ('ToSheet', source.ID)
		connect1.setAttribute ('ToPart', '3') # whole object	
	
		# 2 - connect edge/line to target
		connect2 = self.addElement(connects,'Connect')
		connect2.setAttribute ('FromSheet', edge.ID)
		connect2.setAttribute ('FromPart', '12')
		connect2.setAttribute ('ToSheet', target.ID)
		connect2.setAttribute ('ToPart', '3')	 # whole object	
		
	def addConnectOLD(self, edge, source, target):
		"""
		create the LOGICAL connection between source and target
		- edge - the PHYSICAL connection (the line) is edge
		- source, target - ids, not objects
		
		This is a CONNECTION-BASED connects, which must specify 
		the connection points on the source and target
		objects. 

		This was the only connects understood by Lucid (actually it was ignored)
		"""
		# connects = self.selectSingleNode (self.dom, 'VisioDocument/Pages/Page/Connects')
		# if not connects:
			# raise Exception, 'CONNECTs element not found in VDX'
		parent = self.selectSingleNode (self.dom, 'VisioDocument/Pages/Page')
		if not parent:
				raise Exception, 'Page element not found in VDX'
				
		# get the connection points that our connect will use
		sourceConn = source.getBestConnection(target)
		targetConn = target.getBestConnection(source)
				
		# create the Connects element, which specifies the
		# LOGICAL connection
		# 1 - connect edge/line to source
		connects = self.addElement (parent, 'Connects')
		connect1 = self.addElement(connects, 'Connect')	
		connect1.setAttribute ('FromSheet', edge.ID)
		connect1.setAttribute ('FromPart', '9')
		connect1.setAttribute ('ToSheet', source.ID)
		connect1.setAttribute ('ToPart', '10%s' % 2)		
	
		# 2 - connect edge/line to target
		connect2 = self.addElement(connects,'Connect')
		connect2.setAttribute ('FromSheet', edge.ID)
		connect2.setAttribute ('FromPart', '12')
		connect2.setAttribute ('ToSheet', target.ID)
		connect2.setAttribute ('ToPart', '10%s' % 3)
	
	def addNode (self, klass, args):
		"""
		klass is a shape constructor (e.g., Circle or Rectangle)
		"""
		# print '- addNode: %s' % klass.__name__
		id = self.getShapeId()
		node = klass(id, args)
		self.addShapeObj(node)
		if self.verbose:
			print '... added a node with id: %s (%s)' % (node.ID, type(node.ID))
		return node.ID
	
	def addShapeObj (self, shape):
		"""
		insert provided shape instance into DOM
		"""
		parent = self.selectSingleNode (self.dom, 'VisioDocument/Pages/Page/Shapes')
		if not parent:
			raise xml.dom.NotFoundErr, 'Shapes node not found'
		parent.appendChild(shape.getElement());
		
		self.shapes[shape.ID] = shape
		
		if self.verbose:
			print '.. addShapeObj objed added shape for', shape.ID
		
	
if __name__ == "__main__":

	# component = ComponentRecord ('LINE-PARTS.xml')
	# print component

	vdx = VdxRecord()
	# print vdx
		
	rec_args = {
		'name' : "my rectangle",
		'x' : 2.75,
		'y' : 7,
		'width' : 1.5,
		'height' : 1,
		'line': {
			'weight':2,
			'color':'#ff0000'
		},
		'label': {
			'text':'my rectangle',
			'size':10
		}
	}
	
	circle_args = {
		'name' : "my circle",
		'x' : 5,
		'y' : 5.5,
		'width' : 1.5,
		'height' : 1,
		'label': {
			'text': 'my circle',
			'color': '#0000ff',
			'size':32
		}
	}
	
	# print shape
	circle = vdx.addNode (Circle, circle_args)
	rectangle = vdx.addNode (Rectangle, rec_args)
	
	vdx.addEdge(circle, rectangle, "eats")
	
	if 1:
		out = os.path.join('/Users/ostwald/Desktop/VDX', 'VDX-OUT.vdx')
		vdx.write (out)
		print 'wrote to', out
	elif 0:
		print vdx

