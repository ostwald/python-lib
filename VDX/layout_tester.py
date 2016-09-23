from VDX import getEcoServiceGraphData, LayoutVdxRecord

teacher, section = 'brown', 'Period 2'
PARAMS = {
	'section' : section,
	'teacher' : teacher
}

def processGraph (params, callback=None):
	graphData = getEcoServiceGraphData(params)
	vdx = LayoutVdxRecord(graphData)
	# vdx.showEdgeData()
	print "teacher: %s \n- section: %s\n- group: %s" % (
			params['teacher'], 
			params['section'], 
			params.has_key('group') and params['group'] or '')
	
	print "%d shapes, %s edges" % (len(vdx.shapes.keys()), len(vdx.edges.keys()))

	if callback:
		callback(params, vdx)

def batchProcess ():
	
	for group in [2,3,4,5,6,7,8]:
		PARAMS['group'] = str(group)
		processGraph(PARAMS, writeGraph)
	
def writeGraph (params, vdx):
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

def graphAll ():

	processGraph(PARAMS, writeGraph)
	
if __name__ == '__main__':
	# batchProcess()
	graphAll()
