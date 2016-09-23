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
	
import sys
from PIL import Image
from ImageTools import ImageTool
import os


class ImageLoader:
	"""
	create specified versions of the image at "infile" and writes each of the versions
	to a different subdirectory of "collectionDir", E.g., 
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
		First creates a full-size jpg and then reads this from disk at the base
		image object. This is done because I found that thumbnails created from
		tiff-based images were sometimes low-quality

		"loadMap" defines the sets of images that will be created
		"""

		loadMap = {
			"large": 960,
			"item": 480,
			"thumbnails":130,
			"tiny":90,
			}

		# create full-sized version (converting if necessary to JPEG)
		originalImg = ImageTool(self.infile)
		print self.filename, originalImg.format, "%dx%d" % originalImg.size, originalImg.mode

		fullsizeDir = os.path.join (self.collectionDir, "full")
		if not os.path.exists (fullsizeDir):
			os.mkdir (fullsizeDir)

		print "writing fullsize to ", fullsizeDir
		originalImg.writeAsJpg (destDir=fullsizeDir)

		masterPath = os.path.join(fullsizeDir, self.filename)
		masterImg = ImageTool(masterPath)
		if masterImg is None:
			raise "ImageLoader unable to load master image at :", masterPath

		for imageType in loadMap.keys():
			size = loadMap[imageType]

			# set up the destDir
			destDir = os.path.join (self.collectionDir, imageType);
			if not os.path.exists(destDir):
				os.makedirs (destDir)

			path = os.path.join (destDir, self.filename)
			sizespec = size, size
			print "about to write to DIRECTORY:", destDir

			"""
			first time through write a jpg and then use this im for the
			we do this because resizing of images read from tiffs is bad
			"""
			masterImg.write_sized_image (sizespec, destDir)

			# image debugging
			if 0:
				dbDestDir = "/Users/ostwald/Desktop/tmp/debug/"
				if not os.path.exists(dbDestDir):
					print "creating dir at ", dbDestDir
					os.makedirs (dbDestDir)
				masterImg.targeted_write (os.path.join
									  (dbDestDir, imageType + ".jpg"), sizespec)

class CollectionLoader:
	"""
	load a directory of images ("sourceDir") into a "collectionDir":
	- web-sized images, and
	- thumbnails
	"""
	def __init__ (self, sourceDir, collectionDir):
		self.sourceDir = sourceDir
		self.collectionDir = collectionDir

		if not os.path.isdir (sourceDir):
			print "ERROR: %s is not a directory" % sourceDir
			return
		if not os.path.exists (collectionDir):
			os.mkdir (collectionDir)

	def load (self):

		for filename in os.listdir(self.sourceDir):
			infile = os.path.join (self.sourceDir, filename)
			if not os.path.isfile(infile) or filename[0] == ".":
				print "skipping ", filename
				continue
			imageLoader = ImageLoader (infile, self.collectionDir)
			imageLoader.load()

class Collection:
	def __init__ (self, sourceDir):
		self.sourceDir = sourceDir
		self.name = os.path.split (sourceDir)[1]

class ImageLibLoader:
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

def loadLibrary ():
	imageLib = "/Users/ostwald/Desktop/art"  # where the loaded images will end up
	if not os.path.exists (imageLib):
		os.makedirs(imageLib)

	originalsDir = "/Users/ostwald/AnisArt"   # where the original images are
	bestDir = os.path.join (os.path.join (originalsDir, "Images", "Best"))
	collectionList = [
		Collection (os.path.join (bestDir, "painting")),
		Collection (os.path.join (bestDir, "notecards")),
		Collection (os.path.join (bestDir, "quilting")),
		Collection (os.path.join (bestDir, "photography")),
		]
	
	ImageLibLoader (imageLib, collectionList).load()

def testLoadImage ():
	
	baseDir = "/Users/ostwald/Desktop/tmp"
	outDir = baseDir
	imgPath = os.path.join (baseDir, "original.tif")
	ImageLoader (imgPath, outDir).load()
	print "done"

if __name__ == "__main__":
	"""
	/Users/ostwald/Desktop/AnisArt/Images/Originals/ani iPhoto 06172005
	"""
	# loadLibrary()

	srcdir = "/Pictures/AnisArt/tmp/photos-02242007/"
   	destdir = "/Pictures/AnisArt/Images/image-library/photography"

	CollectionLoader (srcdir, destdir).load()

