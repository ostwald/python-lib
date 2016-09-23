"""
figure out how to make a connecting line between two shapes.

the shapes have connectors, so we can use them as endpoints of the line

First - given a shape, get the x,y coordinates of the connections.

Shape.connections == {'N': (x, y), 'E': (x,y) ..}

Used in drawVDX

"""

import sys, os, math
import util
from line import Line
from connects import Connects

def showConnections (shape):
	conns = shape.getConnections()
	for key in conns.keys():
		# print '- %s (%s)' % (key, conns[key])
		print '- %s (%s, %s)' % (key, conns[key][0], conns[key][1])
		
def makeConnectorShape (fromShape, toShape, relation, id=None):
	"""
	given two endpoints (the connectors) ...
	PinX is midpoint of x's
	PinY is midpoint of y's
	
	this function has to compute the input parameters to
	the Line constructor (to be implemented)
	
	XForm1D is inserted in Shape
	ObjectType = 2
	
	"""
	
	def avg (a, b):
		return (float(a) + float(b)) / 2.00000000
		
	def diff (a, b):
		return (float(a) - float(b))
	
	if 0:
		start = fromShape.getConnection('2')
		end = toShape.getConnection('3')
	else:
		start = fromShape.getBestConnection(toShape)
		end = toShape.getBestConnection(fromShape)
	
	print 'makeConnectorShape source=%s, target=%s' % (fromShape.ID, toShape.ID)
	print ' - start: %f, %f' % (start[0], start[1])
	print ' -   end: %f, %f' % (end[0], end[1])
	
	line_args = {
		'name': 'connector',
		'label':{'text':relation},
		# 'x' : avg (start[0], end[0]),
		# 'y' : avg (start[1], end[1]),
		'x' : start[0],
		'y' : start[1],
		'height' : diff (end[1], start[1]) or util.pt2in(2),
		'width' : diff (end[0],start[0]),
		'begin_x' : start[0],
		'begin_y' : start[1],
		'end_x' : end[0],
		'end_y' : end[1]
	}
	
	print 'line_args'
	for k, v in line_args.iteritems():
		print ' - %s: %s' % (k,v)
	
	return Line (id, line_args)
		
if __name__ == '__main__':
	from vdxRecord import VdxRecord, Circle, Rectangle
	
	shape1 = {
		'name' : "shape1", # this is only true if we add it first
		'x' : 2,
		'y' : 7,
		'label': {'text':'shape1'}
	}
	
	shape2 = {
		'name' : "shape2", # this is only true if we add it first
		'x' : 4,
		'y' : 7,
		'label': {'text':'shape2'}
	}
	
	vdx = VdxRecord()
	fromShapeId = vdx.addNode (Rectangle, shape1)
	fromShape = vdx.getShape(fromShapeId)
	toShapeId = vdx.addNode (Rectangle, shape2)
	toShape = vdx.getShape(toShapeId)	
	conn = makeConnectorShape (fromShape, toShape)
	vdx.addShapeObj (conn)
	
	connects = Connects (conn.ID, fromShapeId, 2, toShapeId, 3)
	vdx.addConnects(connects.element)
	
	if 1:
		out = "VDX-OUT.vdx"
		vdx.write (out)
		print 'wrote to', out
	else:
		print vdx

	

