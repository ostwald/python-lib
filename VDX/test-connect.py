import os, sys
from VDX import VdxRecord, Circle, Line, Rectangle
import util

		
shape_1 = {
	'name' : "shape_1",
	'x' : 1,
	'y' : 9,
	'width' : 1,
	'height' : 1,
	'line': {
		'color':'#008040',
	},
	'label': {
		'color': '#008040',
		'text' : '1'
	}
}

shape_2 = {
	'name' : "shape_2",
	'x' : 3,
	'y' : 9,
	'width' : 1,
	'height' : 1,
	'line': {
		'color':'#0000ff',
	},
	'label': {
		'color': '#0000ff',
		'text' : '2'
	}
}

class ConnectVdxRecord (VdxRecord):
	
	def makeEdgeShape(self, source, target, relation, id):
		"""
		NOTE: if height is zero, we get an angled line that is bent
		at the connector point. it looks good until you move a node and
		the bend shows
		"""
		
		if 0:
			start = (source.PinX, source.PinY)
			end = (target.PinX, target.PinY)
		elif 0:
			start = source.getConnection("N")
			end = target.getConnection("S")
		else:
			start = source.getBestConnection(target)
			end = target.getBestConnection(source)
		print 'makeEdgeShape source=%s, target=%s' % (source.ID, target.ID)
		print ' - start: %f, %f' % (start[0], start[1])
		print ' -   end: %f, %f' % (end[0], end[1])
		
		line_args = {
			'name': '3',
			'label':{
				'text':relation,
				'color':'#ff8000'
			},
			'line' : {
				'color':'#ff8000'
			},
			# 'x' : avg (start[0], end[0]),
			# 'y' : avg (start[1], end[1]),
			'x' : start[0],
			'y' : start[1],
			# 'height' : util.diff (end[1], start[1]) or util.pt2in(2),
			'height' : util.diff (end[1], start[1]) or 0.0001,
			'width' : util.diff (end[0],start[0]),
			'begin_x' : start[0],
			'begin_y' : start[1],
			'end_x' : end[0],
			'end_y' : end[1]
		}
		
		print 'line_args'
		for k, v in line_args.iteritems():
			print ' - %s: %s' % (k,v)
		
		return Line (id, line_args)
		
	def addConnect (self, edge, source, target):
		print "TEST-CONNECT - addConnect()"
		VdxRecord.addConnect(self, edge, source, target);
		

if __name__ == "__main__":

	# component = ComponentRecord ('LINE-PARTS.xml')
	# print component

	vdx = ConnectVdxRecord()
	# shape_class = Rectangle # connector names are not N,S,E,W
	shape_class = Circle # 
	node1 = vdx.addNode (shape_class, shape_1)
	node2 = vdx.addNode (shape_class, shape_2)
	if not node1:
		raise Exception, "node1 not found"
	if not node2:
		raise Exception, "node2 not found"
	vdx.addEdge ('shape_1', 'shape_2', "3")
	
	if 1:
		out = util.getOutput ('VDX-CONNECTION.vdx')
		vdx.write (out)
		print 'wrote to', out
	else:
		print vdx
