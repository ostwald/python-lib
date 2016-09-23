"""
Shapes including Circle and Rectangle
"""

import sys, os, re, copy
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils, MetaDataRecord
import util


class ComponentRecord (XmlRecord, UserDict):
	"""
	reads component metadata and exposes the top
	level elements as a map
	"""
	def __init__ (self, path):
		XmlRecord.__init__ (self, path=path)
		self.data = {}
		for node in XmlUtils.getChildElements(self.doc):
			self[node.nodeName] = node
			
	def __repr__ (self):
		s = ''
		l = [];add=l.append
		for key in self.keys():
			add ('- %s' %  key)
		return '\n'.join(l)
				

class Shape (MetaDataRecord):
	"""
	generic shape class, to be subclassed to add Geometry
	"""
	xpath_delimiter = '/'
	shape_template = util.getTemplate('SHAPE-TEMPLATE')
	component_xml = None # subclasses provide xml file
	
	# there must be an xpath for every value we will write to DOM
	xpaths = {
		'ID': 'Shape/@ID',
		'Name': 'Shape/@Name',
		'Type': 'Shape/@Type',
		'PinX' : 'Shape/XForm/PinX',
		'PinY' : 'Shape/XForm/PinY',
		'Width' : 'Shape/XForm/Width',
		'Height' : 'Shape/XForm/Height',
		'ObjType' : 'Shape/Misc/ObjType',
		'LineWeight' : 'Shape/Line/LineWeight',
		'LineColor' : 'Shape/Line/LineColor',
		'CharSize' : 'Shape/Char/Size',
		'CharColor' : 'Shape/Char/Color',
		'Text' : 'Shape/Text'
	}
	
	# provided shape args override these defaults
	default_shape_args = {
		'name': 'unnamed',
		'x':1,
		'y':1,
		'height':1,
		'width':1,
		'line':{
			'weight':1, 
			'color':'0'
		},
		'label': {
			'text': '',
			'size': 12,
			'color':'0'
		}
	}
		
	
	def __init__ (self, id, args=None):
		MetaDataRecord.__init__ (self, path=self.shape_template)
		# make a copy so we don't stomp default_shape_args
		opts = copy.deepcopy(self.default_shape_args)
		if args is not None:
			util.update(opts, args)
		
		# define all attributes to match xpath mapping above.
		# the xpath mappings determine what attributes are written to DOM.
		self.ID = id	
		self.Name = opts['name']
		self.Type = "Shape"
		self.PinX = opts['x']
		self.PinY = opts['y']
		self.Width = opts['width']
		self.Height = opts['height']
		self.ObjType = 1
		self.LineWeight = util.pt2in (opts['line']['weight'])  #from px to inch
		self.LineColor = opts['line']['color']
			
		self.CharSize = util.pt2in (opts['label']['size'])
		self.CharColor = opts['label']['color']
		self.Text = opts['label']['text']
		
		self.addCustomAttrs(opts)
		
		# inject components
		self.components = ComponentRecord (path=self.component_xml)
		try:
			# assigns components record as side effect
			self.injectComponents()
		except KeyError, msg:
			raise Exception, "ERROR: cannot inject component: %s" % msg
		
		# write element values to DOM
		for attr in self.xpaths:
			try:
				self.set(attr, str(getattr(self, attr)))
			except Exception, msg:
				# print 'WARN: set failed for %s' % attr
				pass

		
		# populate formuliac fields
		self.doFormulas (self.dom)
		self.connections = None

	def addCustomAttrs(self, opts):
		"""
		hook for subclasses to add attributes to be written to
		DOM. xpaths also need to be added
		"""
		pass

	def getConnections (self):
		
		# print 'getConnections'
		if self.connections is None:
			conns = UserDict()
			pinX = float(self.get('PinX'))
			pinY = float(self.get('PinY'))
			# print ' - pinY: %f, pinX: %f' % (pinX, pinY)
			for node in self.selectNodes(self.dom, 'Shape/Connection'):
				id = XmlUtils.getTextAtPath(node, '@ID')
				name = XmlUtils.getTextAtPath(node, '@Name')
				x = float(XmlUtils.getTextAtPath(node, 'X'))
				y = float(XmlUtils.getTextAtPath(node, 'Y'))
				conns[name] = (x+pinX, y+pinY)
				# conns[id] = (x+pinX, y+pinY)
			self.connections = conns
		return self.connections

	# def getConnection (self, connId):
	def getConnection (self, name):
		try:
			# return self.getConnections()[connId]
			return self.getConnections()[name]
		except Exception, msg:
			print "ERROR getConnection: %s", msg
			return None
			
	def getBestConnection (self, target):
		"""
		target is an other shape.
		approach:
		 calculate 
		  - delta_x = target_x - self.x
		  - delta_y = target_y - self.y
		  - m - the slope from this shape to target
		  
			if delta_x == 0 or abs(m) > 1:
				delta_y > 0 ? N : S
			else
				delta_x < 0 ? E : W
		"""
		delta_x = target.PinX - self.PinX
		delta_y = target.PinY - self.PinY
		# all slopes above 1 are treated the same
		# print "delta_x: %f, delta_y: %f" % (delta_x, delta_y)

		slope = delta_x == 0 and 2 or delta_y/delta_x

		conn_name = None
		if abs(slope) > 1: # we know it is steeper than 45% vertical
			conn_name = delta_y > 0 and 'N' or 'S'
		else:
			conn_name = delta_x > 0 and 'E' or 'W'
			
		try:
			# return self.getConnections()[connId]
			return self.getConnections()[conn_name]
		except IOError, msg:
			print "ERROR getBestConnection: %s" % msg
			return None

	def injectComponents (self):
		"""
		All Shapes must have a Geom component, and may have others
		This method injects the Geom component for this shape 
		
		Subclasses may extend:
		  Shape.injectComponents(self)
		  # now do stuff for subclass
		"""
		srcGeom = self.components['Geom']
		if not srcGeom:
			raise DomException, "srcGeom not found in shape components"
		newGeom = srcGeom.cloneNode(1)
		oldGeom = self.selectSingleNode(self.dom, 'Shape/Geom')
		if not oldGeom:
			raise DOMException, 'Geom placeholder not found in Shape Template'
		self.doc.insertBefore(newGeom, oldGeom)
		self.doc.removeChild(oldGeom)

	def doFormulas (self, parent):
		"""
		formulas are expressed as attribute values. 
		e.g., <TxtHeight F="Height*0.861111">
		
		variables used are 'Width' and 'Height', so these must 
		be available to eval
		
		all elements having formulaty ("F") attrs are assigned a text value that
		is the result of evaluating the formula
		"""
		Width = getattr(self, 'Width')
		Height = self.Height
		# print 'Width is a %s' % type(Width)
		for child in XmlUtils.getChildElements(parent):
			f = child.getAttribute("F")
			if f:
				# print '- %s - "%s"' % (child.tagName, f)
				if f.startswith('NURBS'): 
					val = f
				else:
					val = eval(f)
				# print " -> ", val
				XmlUtils.setText (child, str(val))
			if XmlUtils.getChildElements(child):
				self.doFormulas(child)
			
	def getElement (self):
		return self.doc.cloneNode(1)
			
class ConnectedShape (Shape):
	
	def injectComponents (self):
		"""
		inject connections after super class does its thing.
		connections come before TextBlock 
		"""
		Shape.injectComponents(self);
		
		# connections are inserted one at a time as children of shape
		connectorsNode = self.components['Connections']
		if not connectorsNode:
			raise DomException, "Connections not found in components"

		textBlockNodeNode = self.selectSingleNode(self.dom, 'Shape/TextBlock');
		if not textBlockNodeNode:
			raise DomException ("TextXForm not found in Shape");
		
		connectors = XmlUtils.getChildElements (connectorsNode)
		while (connectors):
			connector = connectorsNode.removeChild(connectors[0])
			self.doc.insertBefore(connector, textBlockNodeNode)
			connectors = XmlUtils.getChildElements (connectorsNode)
			
# For draw.io we do NOT define connection points in the shape
# For LucidChart we DID define them, and used ConnectedShape
SHAPE_BASE_CLASS = Shape # ConnectedShape
			
class Rectangle (SHAPE_BASE_CLASS):

	component_xml = util.getTemplate('RECTANGLE-PARTS')
	
class Circle (SHAPE_BASE_CLASS):
	
	component_xml = util.getTemplate('CIRCLE-PARTS')

