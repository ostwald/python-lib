
import os, sys
import util
from JloGraph import Layout
from VDX import VdxRecord, Rectangle, Circle

class DrawVDX:
	
	origin = [5,5] # to place center near center of page
	layout_args = {
		'force_strength':1.5 # determine spread
	}

	def __init__ (self, edges):
		"""
		edges is  a list of dicts containing
		- source, target, relation
		"""
		self.layout = Layout (edges, **self.layout_args)
		print self.layout
	
		self.vdx = self.makeVdxRecord()

	def makeVdxRecord(self):
		vdx = VdxRecord()
	
		# process Nodes - make the args that will create shapes (rectangles) in vdx
		for id, data in self.layout.nodes.iteritems():
			pos = data['location']
			args = {
				'name': id,
				'label': {'text': id },
				'x':pos[0] + self.origin[0],
				'y':pos[1] + self.origin[1], 	
				'width':0.5,
				'height':0.5,
				'color':'#2e62ff'
			}
			
			# print "adding shape at %s, %s" % (args['x'], args['y'])
			id = vdx.addNode(Circle, args)
			shape = vdx.getShape(id)
			if not shape:
				# print vdx
				# print '-----------'
				# print 'shape keys:'
				# for key in vdx.shapes.keys():
					# print ' - %s (%s)' % (key, type(key))
				print "ERROR shape not found for added shape (%s) ... HALTING" % id
				
				sys.exit()
				
			print ' ... (%s - %f, %f)' % (shape.Name, shape.PinX, shape.PinY)
	
		for data in self.layout.edges:
			if 0:
				source = int(data['source'])
				target = int(data['target'])
			else:
				source = data['source']
				target = data['target']
			print 'source: %s target: %s'  % (source, target)
			vdx.addEdge (source, target, data['relation'])
			
		return vdx
	
if __name__ == '__main__':
	edgeData = [
		(1,2,'decomposes'),
		(1,3,'decomposes'),
		(4,1,'produces')
	]
	
	
	edges = [{"source": str(s), "target": str(t),"relation": str(r)} 
	  for s, t, r in edgeData]
	
	graph = DrawVDX(edges)
	
	if 0:
		print graph.vdx
	else:
		# out = '/Users/ostwald/Desktop/VDX/FORCE_LAYOUT.vdx'
		out = util.getOutput ('FORCE_LAYOUT.vdx')
		graph.vdx.write(out)
		print 'wrote to', out
