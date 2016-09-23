"""
VDX utils
"""
import os, collections

def avg (a, b):
	return (float(a) + float(b)) / 2.00000000
	
def diff (a, b):
	return (float(a) - float(b))

def update(d, u):
	"""
	perform "deep" update on dicts
	"""

	for k, v in u.iteritems():
		if isinstance(v, collections.Mapping):
			r = update(d.get(k, {}), v)
			d[k] = r
		else:
			d[k] = u[k]
	return d
    
def pt2in (pt):
	"""
	convert PTs to Inches
	"""
	return float(pt) * 0.0138888888888
	
def getTemplate (template):
	# relative to this package
	return os.path.join (os.path.dirname(__file__), 'template', template+'.xml')
	
def getCsvData (worksheet):
	# relative to this package
	return os.path.join (os.path.dirname(__file__),'bio/data', worksheet+'.csv')
	
def getOutput (filename):
	return os.path.join ('/Users/ostwald/Desktop/VDX', filename)
