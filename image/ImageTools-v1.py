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

class ImageTool:
	def __init__ (self, infile):
		"@sig public ImageLoader(java.lang.String infile, java.lang.String collectionDir)"
		
		self.infile = infile
		print ("ImageTool for ", infile)
		self.dir, self.filename = os.path.split(infile)
		self.name, self.ext = os.path.splitext (self.filename)
		self.im = self.get_image()

	def get_image (self):
		try:
			im = Image.open(self.infile)
			print (self.filename, im.format, "%dx%d" % im.size, im.mode)
			return im
		except IOError:
			print ("couldn't recognize %s as an image")
			return
		
class JpegConverter (ImageTool):
	"""
	PIL's conversion from TIFF to JPEG seems just as good as PhotoShop's
	"""
	def converter (self):
		im = self.im
		format = im.format
		if format != "JPEG":
			try:
				im.save (os.path.join (self.dir, self.name+".jpg"))
			except IOError:
				print ("couldn't save %s as a JPEG image" % self.infile)
				return

class Thumbnailer (ImageTool):

	def thumbnailer (self):
		im = self.im

		format = im.format
		if format == "TIFF":
			print ("WARNING: Original image is of format %s which makes bad thumbnails" % format)

		try:
			thumbsize = 200, 200
			thumbpath =	 os.path.join (self.dir, self.name+"-thumb.jpg")
			im.thumbnail(thumbsize)
			im.save(thumbpath, "JPEG")
		except IOError:
			print ("cannot create thumbnail for", self.filename)

if __name__ == "__main__":
	
	path = "/Users/ostwald/Documents/Comms/web_gallery/Test_1/energy saving/scratch/IMG_1699.CR2"
	Thumbnailer (path).thumbnailer()
	# JpegConverter (path).converter()
