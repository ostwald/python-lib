import sys, os
from misc.DirectoryCompare import Dir, DirCompare

txtDir = "H:/python-lib/SAT_Analysis/txtFiles"
xlsDir = "H:/python-lib/SAT_Analysis/xlsFiles"

class MyDir (Dir):
	def __init__ (self, path):
		Dir.__init__ (self, path);

		myData = []
		for f in self.data:
			myName = f.split('.')[0]
			# print myName
			myData.append (myName)
		self.data = myData

class MyDirCompare (DirCompare):
	def __init__ (self, path1, path2):
		self.dir1 = MyDir(path1)
		self.dir2 = MyDir(path2)
		
		self.union = self._getUnion()
						  
dc = MyDirCompare (txtDir, xlsDir)
dc.report()
