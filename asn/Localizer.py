"""
To localize from command line:
	
	use the stylesheet at ~/bin/xsl/remove-namespaces-and-localize.xsl along
	with the transform script like so:

		~/bin/transform ~/bin/xsl/remove-namespaces-and-localize.xsl 1995-NSES-v1.2.5.xml localized/
"""
import os
import shutil

LOCALIZED = "localized"
ORIGINAL = "original"

cmd = "/home/ostwald/bin/transform"
script = "/home/ostwald/bin/xsl/remove-namespaces-and-localize.xsl"
stdsBase = "/home/ostwald/asn-standards-docs"



def localizeDir (dir):
	print "\nlocalizing " + dir
	if not os.path.exists(dir):
		raise "DirDoesNotExist", dir
	topic = os.path.split(dir)[1]
	
	stds = os.listdir (dir)
	i = 0
	for filename in stds:
		i += 1
		root, ext = os.path.splitext(filename)
		if ext.lower() != ".xml": continue
		if filename.find (" ") != -1:
			newname = filename.replace (" ", "_")
			os.rename (os.path.join (dir, filename), os.path.join (dir, newname))
			filename = newname
			
		dst = getPath (LOCALIZED, topic, filename)
		if os.path.exists (dst):
			print "%s exists" % dst
			continue
		print "\n %d/%d %s" % (i, len(stds), filename)
		localize (topic, filename)
		
		
			
def localize (topic, std):
	
	src = getPath (ORIGINAL, topic, std)
	dst = getPath (LOCALIZED, topic, std)
	
	dstDir = os.path.dirname (dst)
	
	if not os.path.exists (dstDir):
		print "%s does not exist" % dstDir
		os.makedirs(dstDir)
	
	command = "%s %s %s %s" % (cmd, script, src, dstDir)
	# print command
	os.system(command)
	
def getPath (target, topic, std):
	if target not in [LOCALIZED, ORIGINAL]:
		raise "Unknown Target", target
	return os.path.join (stdsBase, target, topic, std)

if __name__ == "__main__":
	std = "2005-South Dakota-Science.xml"
	topic = "science"
	# localize (topic, std)
	
	dir = os.path.join (stdsBase, ORIGINAL, topic)
	localizeDir (dir)

