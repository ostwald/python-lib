from UserDict import UserDict

class Colors (UserDict):
	
	orgTypeColors = {
		'mammal' : {
			'line' : '#264987',
			'text' : '#264987',
			'fill' : ''
		},
		'insect' : {
			'line' : '#701500',
			'text' : '#701500',
			'fill' : ''
		},
		'bird' : {
			'line' : '#077fff',
			'text' : '#077fff',
			'fill' : ''
		},	
		'reptiles/amphibian' : {
			'line' : '#264987',
			'text' : '#264987',
			'fill' : ''
		},	
		'plant' : {
			'line' : '#61645d',
			'text' : '#61645d',
			'fill' : ''
		},	
		'decomposer' : {
			'line' : '',
			'text' : '',
			'fill' : ''
		}
	}
	
	def __init__ (self):
		self.data = self.orgTypeColors
		if 0:
			print 'Colors'
			for key, val in self.iteritems():
				print '%s' % key
				for obj, objVal in self[key].iteritems():
					print '- %s: %s ' % (obj, objVal)
	
	def __getitem__(self, key):
		if not self.data.has_key(key):
			return None
		return self.data[key]
	
	def getColor(self, orgType, obj, default=None):
		if not self[orgType]:
			return None
		if not self[orgType].has_key(obj):
			return None
		return self[orgType][obj]
