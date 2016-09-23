"""
File system abstractions
	- JloFSObj - abstract file system class
	- JloFile
	- JloDir
	
These classes will form the basis of a tool kit for working with files
and directories (e.g., CVS tools, directory compare, etc)

Compare model: CVS: Working vs Reference
"""
import sys, os
from UserDict import UserDict
import Carbon.File
import directory_compare
from directory_compare import time_helpers
import myglobals

class JloFSCache (UserDict):
	
	def __init__ (self):
		UserDict.__init__ (self)
	
	def add (self, fsObj):
		self[fsObj.path] = fsObj
		
	def get (self, path):
		if not path in self.data.keys:
			raise Exception, "JloFSCache: Object not found for %s" % path
		return self[path]

FS_OBJ_CACHE = JloFSCache()
		
class JloFSObj:
	def __init__ (self, path, level=0):
		if path.endswith('/'): path = path[:-1]
		self.path = path
		self.level = level
		self.dirname, self.name = os.path.split(path)
		self.root, self.ext = os.path.splitext(self.name)
				
		## stat = os.stat(path)
		self.modtime = os.path.getmtime(path)
		self.ctime = os.path.getctime(path)
		self.size = os.path.getsize(path)
		self.islink = os.path.islink(path)
		self.isalias = self._isAliasFile(path)
		self.exists = os.path.exists(path)
		
		#if not os.path.exists(path):
		#	raise Exception, "File Obj does not exist at %s" % path
			
	def newerthan (self, other):
		# print "%d > %d??" % (self.modtime, other.modtime)
		return self.modtime > other.modtime
		
	def _isAliasFile (self, path):
		fsspec = Carbon.File.FSSpec (path)
		return fsspec.IsAliasFile()[0]
		
		FS_OBJ_CACHE.add (self)
		
	def ppDate (self, secs):
		return time_helpers.toStr (secs)
		
	def __repr__ (self):
		s=[];add=s.append
		## add ("JloFSObj")
		add ("path: %s" % self.path)
		add ("name: %s" % self.name)
		add ("root: %s, ext: %s" % (self.root, self.ext))
		add ("lastMod: %s" % self.ppDate (self.modtime))
		if self.islink: add ("link")
		if self.isalias: add ("alias")
		add ("--------------------")
		return "\n".join (s)
		
	def simplelisting (self):
		# return ("%s %s" % (self.name, self.ppDate (self.modtime)))	
		label = self.name
		if self.islink:
			label = "%s (link)" % label
		if self.isalias:
			label = "%s (alias)" % label
		return "%s %s" % (myglobals._padStr (self.name, 40), 
						  myglobals._padStr (self.ppDate (self.modtime), 25, 'right'))
				
						  
	def listing (self):
		# return ("%s %s" % (self.name, self.ppDate (self.modtime)))	
		label = self.name
		if self.islink:
			label = "%s (link)" % label
		if self.isalias:
			label = "%s (alias)" % label
		return "%s*%s (%s)" % (myglobals.getIndent(self.level), 
							   self.name, 
							   self.ppDate (self.modtime))
		
	def _sort_val (self, attr):
		"""
		value used to sort Files by
		"""
		if not hasattr (self, attr):
			return None
		val = getattr (self, attr)
		if type(val) == type(""):
			val = val.lower()
		return val
		
class JloFile (JloFSObj):
	
	def __init__ (self, path, level=0):
		JloFSObj.__init__ (self, path, level)
		self.name = os.path.basename (self.path)
		self.root, self.ext = os.path.splitext(self.name)
		self._content = None
		
	def equals (self, other):
		# print "equals (%s, %s)" % (self.name, other.name)
		ret = (self.getContent() == other.getContent())
		# print " --> %s" % ret
		return ret
		
	def __repr__ (self):
		s = [];	add = s.append
		add ("\nJloFile")
		add (JloFSObj.__repr__ (self))
		return "\n".join (s)
		
class JloDirectory (JloFSObj, UserDict):
	
	"""
	Contents - UserDict mapping path to children (files and directories)
	"""
	
	recurse = 1
	skip_names = ['.DS_Store', '.localized', 'CVS', 'build']

	def __init__ (self, path, level=0):
		UserDict.__init__(self)
		JloFSObj.__init__(self, path, level)
		
		for filename in os.listdir(self.path):
			# print "filename: " + filename
			if not self._accept_file (filename):
				continue
				
			fpath = os.path.join (self.path, filename)
			if os.path.isdir (fpath):
				if self.recurse:
					obj = self.getDirectory (fpath)
				else:
					# obj = self.getDirectory (fpath)
					obj = JloFSObj (fpath)
					# print "subdir: " + fpath
			elif os.path.isfile(fpath):
				obj = self.getFile (fpath)
			else:
				print fpath, "skipped"
				continue
			if filename.strip():
				self[filename] = obj
			
	def getDirectory (self, path):
		return JloDirectory (path, self.level+1)
		
	def getFile (self, path):
		return JloFile (path, self.level+1)
		
	def getfiles (self):
		files = []
		for item in self.dir():
			if isinstance (item, JloFile):
				files.append (item)
		return files
		
	def getsubdirs (self):
		dirs = []
		for item in self.dir():
			if isinstance (item, JloDirectory):
				dirs.append (item)
		return dirs
		
	def isempty (self):
		return (len(self) == 0)
		
	def hasitem (self, filename):
		return filename in self.keys()
		
	def getitem (self, filename):
		if self.has_key (filename):
			return self[filename]
				
	def dir (self, attr="name", ascending=0):
		list = self.values()

		mycmp = lambda a,b: cmp(a._sort_val(attr), b._sort_val (attr))
		list.sort (mycmp)
		
		if ascending:
			list.reverse()
		return list
			
	def __repr__ (self):
		s=[];add=s.append
		add ("\nJloDirectory")
		add (JloFSObj.__repr__ (self))
		for obj in self.dir('lastmod', 0):
			## add (str (obj))
			add (obj.listing())
		return '\n'.join (s)
			
	def simplelisting (self):
		s=[];add=s.append
		add ("** %s" % self.name)
		for obj in self.dir():
			add (obj.listing())
		return '\n'.join (s)
		
	def listing (self):
		s=[];add=s.append
		add ("%s%s" % (myglobals.getIndent(self.level), self.name))
		for obj in self.dir():
			add (obj.listing())
		return '\n'.join (s)
		
	def _accept_file (self, filename):
		"""
		Icon files (are they mac or pc files?) are named "Icon", 
		but there is a chr(13) at the end - we want to reject these!
		"""
		if filename.endswith ("Icon" + chr(13)):
			return 0
		if filename.startswith ("."): return 0
		if filename.startswith (".DS_Store"): return 0
		return not filename in self.skip_names

def testIconPath (path):
	print "TEST ICON PATH: " + path
	for letter in path:
		print "'%s' ord: '%d'  hex: '%s'" % (letter, ord(letter), hex(ord(letter)))
		# print "'%s'" % hex(22)
	print 'chr(13): "%s"' % chr(13)
	
	if path.endswith (chr(13)):
		print 'path ends with chr(13)'
		
	if path.endswith ("Icon" + chr(13)):
		print 'path ends with Icon + chr(13)'
		
def fsObjTester ():
	path = "/Users/ostwald/devel/projects/dcs-project/"
	
	obj = JloFSObj (path)
	print obj
	
def fileTester ():
	file = "/Users/ostwald/devel/projects/dcs-project/build.xml"
	link = "/Users/ostwald/projects" 
	alias = "/Users/ostwald/Movies" 
	icon = "/Users/ostwald/devel/projects/Icon"
	path = icon
	obj = JloFile (path)
	print obj.listing()
		
def dirTester ():
	path = "/Users/ostwald/projects" 
	path = "/Users/ostwald/devel/projects/dlese-tools-project/src/org/dlese/dpc/schemedit"
	# path = "/Users/ostwald/devel/tmp/" 
	obj = JloDirectory (path)
	print obj
	
if __name__ == "__main__":
	dirTester ()
	#fileTester ()
