"""
To transform from command line:
	
	use the stylesheet at ~/bin/xsl/remove-namespaces-and-localize.xsl along
	with the transform script like so:

		~/bin/transform ~/bin/xsl/remove-namespaces-and-localize.xsl 1995-NSES-v1.2.5.xml localized/
"""
import os
import shutil

class Transformer:
	
	def __init__ (self, cmd, xsl, srcDir, dstDir):
		self.cmd = cmd
		self.xsl = xsl
		self.srcDir = srcDir
		self.dstDir = dstDir
	
	def transform (self, src):
	
		if not os.path.exists (self.dstDir):
			print "%s does not exist" % self.dstDir
			os.makedirs(self.dstDir)
		
		command = "%s %s %s %s" % (self.cmd, self.xsl, src, self.dstDir)
		# print command
		os.system(command)

	def transformDir (self):
		self.transform (self.srcDir)
		

		
	def transformDir_BOG (self):
		srcDir = self.srcDir
		dstDir = self.dstDir
		
		print "\ntransforming " + srcDir
		if not os.path.exists(srcDir):
			raise "DestDirDoesNotExist", srcDir
		
		filenames = os.listdir (srcDir)
		i = 0
		for filename in filenames:
			i += 1
			root, ext = os.path.splitext(filename)
			if ext.lower() != ".xml": continue
			if filename.find (" ") != -1:
				newname = filename.replace (" ", "_")
				os.rename (os.path.join (srcDir, filename), os.path.join (srcDir, newname))
				filename = newname
				
			dst = os.path.join (dstDir, filename)
			if os.path.exists (dst):
				print "%s exists - not overwriting" % dst
				continue
			print "\n %d/%d %s" % (i, len(filenames), filename)
			self.transform (os.path.join (srcDir, filename))
		
def adn2nsdl_dc ():
	cmd = "/home/ostwald/bin/transform"
	xsl = "/home/ostwald/bin/xsl/adn-v0.6.50-to-nsdl_dc-v1.02-asn-identifiers-mime.xsl"
	dstDir = "/home/ostwald/python-lib/misc/common-nsdl_dc"
	srcDir = "/home/ostwald/python-lib/misc/common-ADN"
	
	t = Transformer (cmd, xsl, srcDir, dstDir)
	# t.transform (os.path.join (srcDir, "SAT-000-000-000-035.xml"))
	t.transformDir()

if __name__ == "__main__":
	
	adn2nsdl_dc ()

