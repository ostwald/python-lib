"""
File system abstractions
	- JloFSObj - abstract file system class
	- JloFile
	- JloDirectory
	
These classes will form the basis of a tool kit for working with files
and directories (e.g., CVS tools, directory compare, etc)

Compare model: CVS: Working vs Reference
"""
import sys, os, time
from UserDict import UserDict
import myglobals

class JloFSCache (UserDict):
	"""
	A mapping of file path to JloFSObj.
	"""
	def __init__ (self):
		UserDict.__init__ (self)
	
	def add (self, fsObj):
		# print "cache adding %s\n\t%s" % (fsObj.__class__.__name__, fsObj.path)
		self[fsObj.path] = fsObj
		
	def get (self, path):
		if not path in self.data.keys():
			raise Exception, "JloFSCache: Object not found for %s" % path
		return self[path]

FS_OBJ_CACHE = JloFSCache()
		
class JloFSObj:
	"""
	Generic file system object. Extended by JloFile and JloDirectory
	exposes
	- path
	- root, ext
	- name, dirname

	- modtime, ctime, size, islink, isalias, exists
	- level (i think this is relative to starting position in a traversing operation)
	"""
	def __init__ (self, path, level=0):
		"""
		normalize path
		raise an exception if the fs object does not exist at path
		
		ADDS ITSELF TO THE CACHE
		
		TODO: rename listing as __repr__ (here and upward in the class hierarchy)
		"""
		if path.endswith('/'): path = path[:-1]
		self.path = path
		if not self.exists():
			raise Exception, "File does not exist at %s" % self.path
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
			
	def exists (self):
		return os.path.exists(self.path)
		
	def newerthan (self, other):
		# print "%d > %d??" % (self.modtime, other.modtime)
		return self.modtime > other.modtime
		
	def _isAliasFile (self, path):
		return 0
		
		
	def ppDate (self, secs):
		return time.asctime(time.localtime(secs))
		
	def toString (self):
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
		
	def alternateRepr (self):
		# return ("%s %s" % (self.name, self.ppDate (self.modtime)))	
		label = self.name
		if self.islink:
			label = "%s (link)" % label
		if self.isalias:
			label = "%s (alias)" % label
		return "%s %s" % (myglobals._padStr (self.name, 40), 
						  myglobals._padStr (self.ppDate (self.modtime), 25, 'right'))
				
						  
	def __repr__ (self):
		"""
		Generic string representation for File system objects. 
		Indented by "self.level"
		"""
		# return ("%s %s" % (self.name, self.ppDate (self.modtime)))	
		label = self.name
		if self.islink:
			label = "%s (link)" % label
		if self.isalias:
			label = "%s (alias)" % label
		return "%s%s (%s)" % (myglobals.getIndent(self.level), 
							   self.name, 
							   self.ppDate (self.modtime))
		
	def _sort_val (self, attr):
		"""
		Gets the value of specified attribute from this 
		JloFSObj instance.
		"""
		if not hasattr (self, attr):
			return None
		val = getattr (self, attr)
		if type(val) == type(""):
			val = val.lower()
		return val
		
class JloFile (JloFSObj):
	"""
	Mainly adds the ability to 
	- examine file contents  (getContents)
	- compare with other files(equals)
	
	NOTE: we fail at binary files!
	"""
	def __init__ (self, path, level=0):
		JloFSObj.__init__ (self, path, level)
		self._content = None
		
	def getContent (self):
		"""
		lazy read as DOC, converted to unix, and cached as self._content
		"""
		if self._content is None:
			lines = map (lambda x:x.rstrip(), open (self.path, 'r').readlines())
			# s = open (self.path, 'r').read()
			# lines = s.split ('\r\n')
			self._content = '\n'.join (lines).rstrip() + '\n'
			# print "%d lines read" % len (lines)
		return self._content
		
	def equals (self, other):
		"""
		Compares the content of two files as strings
		"""
		# print "\nequals (%s, %s)" % (self.name, other.name)
		#  print "self.size: %s other size: %s" % (self.size, other.size)
		ret = (self.getContent() == other.getContent())
		# print "  equals returning %s" % ret
		return ret
		

		
class JloDirectory (JloFSObj, UserDict):
	
	"""
	Directory items (files and directories) are managed as a UserDict that maps path to items
	
	skip_names - directories with these names will not be read
	recurse - determines whether recursive (True by default)
	"""
	
	recurse = 1
	maxdepth = 100
	file_constructor = JloFSObj # constructor for file objects
	
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
				if self.recurse or level < self.maxdepth:
					obj = self.getDirectory (fpath)
				else:
					# obj = self.getDirectory (fpath)
					obj = self.getFile (fpath)
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
		return self.file_constructor (path, self.level+1)
		
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
			
	def alternateRepr (self):
		s=[];add=s.append
		add ("\nJloDirectory")
		add (JloFSObj.__repr__ (self))
		for obj in self.dir('lastmod', 0):
			## add (str (obj))
			add (obj.listing())
		return '\n'.join (s)
		
	def __repr__ (self):
		s=[];add=s.append
		add ("%s%s/" % (myglobals.getIndent(self.level), self.name))
		for obj in self.dir():
			add (str(obj))
		return '\n'.join (s)
		
	def _accept_file (self, filename):
		"""
		Icon files (are they mac or pc files?) are named "Icon", 
		but there is a chr(13) at the end - we want to reject these!
		"""
		if filename.endswith ("Icon" + chr(13)):
			return 0
		if filename[-1] in ['~']: return 0
		if filename[0] in [".", "#"]: return 0
		if filename.startswith ("."): return 0
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
	path = file
	obj = JloFile (path)
	print obj
		
def dirTester ():
	path = "/Users/ostwald/projects" 
	print "PATH: " + path
	# path = "/Users/ostwald/devel/tmp/" 
	obj = JloDirectory (path)
	print obj
	
if __name__ == "__main__":
	# dirTester ()
	fileTester ()
