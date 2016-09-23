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
	

from PIL import Image
import os
import sys

class ImageTool:

	scratchDir = "/Users/ostwald/tmp"
	
	def __init__ (self, infile):
		"@sig public ImageLoader(java.lang.String infile, java.lang.String collectionDir)"
		
		self.infile = infile
		print "ImageTool for ", infile
		self.dir, self.filename = os.path.split(infile)
		self.name, self.ext = os.path.splitext (self.filename)
		self.im = self.read()
		self.size = "unknown"
		self.mode = "unknown"
		self.format = "unknown"
		if self.im:
			self.size = self.im.size
			self.mode = self.im.mode
			self.format = self.im.format

	def get_image (self):
		return self.im

	def read (self):
		try:
			im = Image.open(self.infile)
			## print self.filename, im.format, "%dx%d" % im.size, im.mode
			return im
		except IOError:
			print "couldn't recognize %s as an image"
			return

	def targeted_write (self, path, sizespec):
		im = Sizer (self.im).get_image(sizespec)
		try:
			im.save(path, "JPEG")
		except IOError:
			print "ImageTool cannot targeted_write image to ", path		

	def write (self, im, destDir):
		path = os.path.join (destDir, self.filename)
		try:
			im.save(path, "JPEG")
		except IOError:
			print "ImageTool cannot write image to ", path

	def write_sized_image (self, sizespec=None, destDir=None):
		if sizespec is None:
			return
		if destDir is None:
			destDir = self.scratchDir
		## print "write_sized_image, destDir is ", destDir
		im = Sizer (self.im).get_image(sizespec)
		self.writeAsJpg (im,destDir)

	def writeAsJpg (self, im=None, destDir=None):
		"""
		format is changed by writing to a file
		"""
		if destDir is None:
			destDir = self.scratchDir
		if im is None:
			im = self.im
		destPath = os.path.join (destDir, self.name+".jpg")

		format = im.format

		try:
			im.save (destPath)
			pass
		except IOError:
			print "couldn't save \n\t%s as a JPEG image in\n\t%s" % \
				  (self.infile, destPath)
			return

class Sizer:

	def __init__ (self, im):
		self.im = im.copy()
	
	"""
	returns a resized image
	"""
	def get_image (self, sizespec=(200, 200)):
		im = self.im

		format = im.format
		if format == "TIFF":
			print "WARNING: Original image is of format %s which makes bad thumbnails" % format

		try:
			im.thumbnail(sizespec, Image.ANTIALIAS)
			return im
		except IOError:
			print "Sizer could not resize image"

if __name__ == "__main__":
	
	path = "/Users/ostwald/Desktop/venice.tif"
	## Thumbnailer (path).thumbnailer()
	im = ImageTool (path)
	print im.filename, im.format, "%dx%d" % im.size, im.mode
	im.writeAsJpg ()
	
