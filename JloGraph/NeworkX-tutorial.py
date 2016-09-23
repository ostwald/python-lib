"""
working through example at:
http://networkx.github.io/documentation/latest/tutorial/tutorial.html
"""

import networkx as nx

# create graph
G=nx.Graph()

## NODES
# add a node
G.add_node(1)

#ad a list of nodes
G.add_nodes_from([2,3,4])

# make another graph H
H=nx.path_graph(10)

# add all the nodes of H as nodes of G
G.add_nodes_from(H)

# add_nodes_from takes any "nbunch"
#  - see http://networkx.github.io/documentation/latest/reference/glossary.html#term-nbunch

# add H as a node in G
G.add_node(H)

## EDGES
G.add_edge(1,2)

# I believe edges can be anything.
# Ours will need relationName and id

e = (2,3)
G.add_edge(*e)
# (*tuple) "unpacks a tuple"

G.add_edges_from([(1,2),(1,3)])
G.add_edges_from(H.edges())
# add_edges_from takes any "nbunch"
#  - see
#  http://networkx.github.io/documentation/latest/reference/glossary.html#term-nbunch

# DESTROY
# G.remove_node(H)
# G.clear()

# QUERY
print 'number of nodes',G.number_of_nodes()
print 'number of edges', G.number_of_edges()

print 'nodes:', G.nodes()
print 'edges:', G.edges()

print 'neighbors of 1:', G.neighbors(1)
print 'neighbors of 3:', G.neighbors(3)

# SUBSCRIPT notation and ATTRIBUTES
# when you access an object, the data dict is returned
#  - data dict is empty by default
G.add_edge(1,3)
G[1][3]['color']='blue'
print 'G[1][3]:', G[1][3]

# attributes for graph, node and edge
G = nx.Graph(day="Friday") # at init
G.graph['day']='Monday' # after init

# NOTE: 'weight' is special attribute for edges (a number)

# DIRECTED GRAPHS
# adds methods incl, out_edges(), in_degree, predecessors, successors
print '\nDIRECTED GRAPHS'
DG=nx.DiGraph()
DG.add_weighted_edges_from([(1,2,0.5), (3,1,0.75)])

def showNodes(DG):
	print 'DIRECTED GRAPH NODES'
	for node in DG.nodes():
		showNode(node, DG)

def showNode(n, DG):
	print 'NODE:', n
	print '- out_degree:', DG.out_degree(n,weight='weight')
	print '- degree:', DG.degree(n,weight='weight')
	print '- successors:',DG.successors(n)
	print '- neighbors:', DG.neighbors(n)
	
# print DG.nodes()
# print '\n'.join(map (str, DG.nodes()))

def showEdges(G):
	print 'EDGES'
	for edge in G.edges_iter():
		print '- %s (%s)' % (edge, G[edge[0]][edge[1]])

showEdges(DG)
showNodes(DG)

