"""
Force Layout
https://github.com/dhotson/springy/blob/master/springy.js

Simple Algoritm - http://cs.brown.edu/~rt/gdhandbook/chapters/force-directed.pdf

Python support for force algorithm: package iGraph - stripped of it's
viewer, which requires other stuff requiring fresh python install, which
i don't want to bother with right now.
-  see https://github.com/patrickfuller/igraph/tree/master/python

i graph supplies a force_directed_layout module
igraph.force_directed_layout that contains a method "run" with the following signature

def run(edges, iterations=1000, force_strength=5.0, dampening=0.01,
        max_velocity=2.0, max_distance=50, is_3d=True)
     
# igraph - http://igraph.org/python/
# layout module - http://igraph.org/python/doc/igraph.layout.Layout-class.html
# are these links for the same version I am using??     
"""
import igraph

import igraph.force_directed_layout as layout

import sys
import json
import igraph.json_formatter as json_formatter

class Layout:
	"""
	creates a force-directed layout
	
	exposes
	- edges - e.g., [{ "source": "1", "target": "2" },..]
	- nodes - e.g., "1": { "location": [ 0.094, -0.284, 0.000 ] }, ..}
	"""
	default_args = {
		'iterations' : 1000, 
		'force_strength' : 5.0, 
		'dampening' : 0.01,
        'max_velocity' : 2.0, 
        'max_distance' : 50,
        "is_3d" : False
	}
	def __init__ (self, edges, **args):
		self.edges = edges
		args = args or {}
		opts = self.default_args.copy()
		# print '%d options' % len(opts)
		opts.update(args)
		
		# Generate nodes
		self.nodes = layout.run(edges, **opts)

	def __repr__ (self):
		return json_formatter.dumps({"edges": self.edges, "nodes": self.nodes})


if __name__ == '__main__':
	
	edgeData = [(1,2), (1,3), (3,1)]
	edges = [{"source": str(s), "target": str(t)} for s, t in edgeData]

	layout = Layout (edges)
	print layout

