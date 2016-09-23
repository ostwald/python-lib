"""
    ImageLoader

	collection
	  images
	    image1
	      ..
	    imageN
      thumbnails
	   thumnail1
	   thumnailN	   
"""
	

import Image
import os
import sys

class ImageLoader:
	"""
	create twp versions of the image at "infile" and writes each of the versions
	to a different subdirectory of "collectionDir"
	- big (bigsize) --> images
	- thumbnail (thumbsize) --> thumbnails
	""" 
	def __init__ (self, infile, collectionDir):
		self.infile = infile
		self.collectionDir = collectionDir
		print "loader for ", infile
		filename = os.path.split(infile)[1]
		self.name, self.ext = os.path.splitext(filename)
		self.filename = self.name+".jpg"

	def load (self):
		"""
		using the base image, create variants of it and save them to disk
		"""
		im = ImageTool(self.infile)
		print self.filename, im.format, "%dx%d" % im.size, im.mode
			
		imageDir =  os.path.join (self.collectionDir, "images");

		# set up the image and thumbnail direcotories 
		if not os.path.exists(imageDir):
			os.makedirs (imageDir)

		thumbnailDir = os.path.join (self.collectionDir, "thumbnails");
		if not os.path.exists(thumbnailDir):
			os.makedirs (thumbnailDir)

		try:
			bigsize = 640, 640
			bigpath = os.path.join (imageDir, self.filename)
			big = im.copy()
			big.thumbnail (bigsize)
			big.save (bigpath, "JPEG")
		except IOError:
			print "cannot create image for", self.filename

		try:
			thumbsize = 200, 200
			thumbpath =	 os.path.join (thumbnailDir, self.filename)
			im.thumbnail(thumbsize)
			im.save(thumbpath, "JPEG")
		except IOError:
			print "cannot create thumbnail for", self.filename

class CollectionLoader:
	"""
	load a directory of images ("sourceDir") into a "collectionDir":
	- web-sized images, and
	- thumbnails
	"""
	def __init__ (self, sourceDir, collectionDir):
		self.sourceDir = sourceDir
		self.collectionDir = collectionDir

		if not os.path.isdir(sourceDir):
			print "ERROR: %s is not a directory" % sourceDir
			return

	def load (self):

		for filename in os.listdir(self.sourceDir):
			infile = os.path.join (self.sourceDir, filename)
			imageLoader = ImageLoader (infile, self.collectionDir)
			imageLoader.load()

class Collection:
	def __init__ (self, sourceDir):
		self.sourceDir = sourceDir
		self.name = os.path.split (sourceDir)[1]

class ArtLoader:
	"""
	loads a series of image directories into "collections" according to a
	collectionList, which specifies the source directories for each
	collection. The destination ("collectionDir") a subdirectory of "rootDir"
	and is passed into the constructor.
	"""
	
	def __init__ (self, rootDir, collectionList):
		self.collectionList = collectionList
		self.rootDir = rootDir

	def load (self):
		for c in self.collectionList:
			destDir = os.path.join (self.rootDir, c.name)
			CollectionLoader (c.sourceDir, destDir).load()

if __name__ == "__main__":
	"""
	/Users/ostwald/Desktop/AnisArt/Images/Originals/ani iPhoto 06172005
	"""
	rootDir = "/Users/ostwald/Desktop/art"
	anisartDir = "/Users/ostwald/AnisArt"
	collectionList = [
#		Collection (os.path.join (anisartDir, "Images", "Best", "painting")),
#		Collection (os.path.join (anisartDir, "Images", "Best", "notecards")),
		Collection (os.path.join (anisartDir, "Images", "Best", "quilting")),
#		Collection (os.path.join (anisartDir, "Images", "Best", "photography")),
		]
	
	ArtLoader (rootDir, collectionList).load()



