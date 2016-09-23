"""
Parses property files and retrieves properties
"""

import re
from UserDict import UserDict

class Properties (UserDict):
	
	propSubPat = re.compile ('\$\{(.*?)\}')
	
	def __init__ (self, path):
		self.data = {}
		self.params = {}
		self.path = path
		self.read ()
		
	def read (self):
		
		lines = open(self.path, 'r').readlines()
		self.params = {}
		for line in lines:
			line = line.strip()
			if len(line) < 1 or line[0] == '#':
				continue
			tokens = map (lambda x:x.strip(), line.split('='))
			if not len(tokens) == 2:
				raise Exception, 'Could not parse line: "%s"' % line
			key = tokens[0]
			value = tokens[1]
			
			# collect params into a dict
			if key.startswith('params.'):
				paramName = key[len('params.'):]
				self.params[paramName] = self.doSub(value)
			else:
				self[key] = self.doSub(value)
				

	def doSub (self, val):
		"""
		Substitues assigned property values for "${<property>}" notation
		"""
		# print 'doSub: "%s"' % val
		i = 0
		buf = ''
		while i < len(val):
			m = self.propSubPat.search (val, i)
			if m:
				buf += val[i:m.start()]			
				key = m.group(1)
				# print 'matched on %s -> "%s"' % (key, m.group())
				if self.has_key(key):
	
					buf += self[key]
					# print 'buf is now "%s"' % buf
				else:
					# unknown key
					buf += m.group()
				i = m.end()
			else:
				buf += val[i:]
				break
		return buf
			
	def getProperty (self, prop, default=None):
		"""
		return the named property or the default if property not found
		"""
		if self.has_key(prop):
			return self[prop]
		return default

	def hasProperty (self, prop):
		return self.has_key(prop)

if __name__ == '__main__':
	props = Properties ('myprops.properties')
	if not props.params:
		print 'NO PARAMS'
	else:
		print 'YES'
