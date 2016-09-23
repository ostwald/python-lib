import sys, os
from UserList import UserList
from UserDict import UserDict

class Asset:

	def __init__ (self, path):
		self.path = path
		self.filename = os.path.basename(self.path)
		self.id = self.filename
		root = os.path.splitext(self.filename)[0]
		splits = root.split('_')
		self.year = splits[0]
		self.firstName = splits[2]
		self.lastName = splits[1]		
		self.key = self.lastName + '_' + self.firstName + '_' + self.year
		
	def getYear (asset):
		return asset.split('_')[0]

	def getName (asset):
		root = os.path.splitext(asset)[0]
		return root[5:]

	def __repr__ (self):
		# return self.filename
		return "%s, %s (%s)" % (self.lastName, self.firstName, self.year)

class SoarsAssets (UserDict):

	def __init__ (self, basedir):
		UserDict.__init__ (self)
		self.basedir = basedir

		for year in os.listdir(basedir):
			yeardir = os.path.join (basedir, year)
			for filename in os.listdir (yeardir):
				path = os.path.join (yeardir, filename)
				self.add (Asset (path))

	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted

	def add (self, asset):
		key = asset.key
		if self.has_key(key):
			# raise KeyError, "Duplicate Key for %s" % key
			print "Duplicate Key for %s" % key
		else:
			self[key] = asset

	def __repr__(self):
		s=[];add=s.append
		for key in self.keys():
			add (str(self[key]))
		return '\n'.join (s)


	def getAssetByKey (self, lastName, firstName, year):
		key = '_'.join([lastName, firstName, year])
		return self[key]
		
	def findAsset (self, lastName, firstName=None, year=None):
		matches = []
		for asset in self.values():
			if asset.lastName != lastName:
				continue
				
			if firstName and asset.firstName != firstName:
				continue
				
			if year and asset.year != year:
				continue
				
			matches.append(asset)
				
		return matches

class SoarsAssetsFromTextFile (SoarsAssets):
	
	default_textfile = "data/soars-assets.txt"
	
	def __init__ (self, textfile=None):
		self.textfile = textfile or self.default_textfile
		UserDict.__init__ (self)

		s = open(self.textfile).read()
		lines = s.split('\n')
		print "%d lines read" % len(lines)
		for path in lines:
			if path.strip():
				self.add (Asset (path))

if __name__ == '__main__':

	# assets = SoarsAssets ("C:/Documents and Settings/ostwald/devel/SOARS assets")
	assets = SoarsAssetsFromTextFile ()
	
	print assets.findAsset('Sands', year="2001")
	
	# print assets
