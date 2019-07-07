import sys, os
if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python")


from HyperText.HTML import *
from HyperText.Documents import Document

class HtmlDocument (Document):
	
	DOCTYPE = Markup("DOCTYPE",
				 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"')
	
	def __init__ (self, *content, **attrs):
		if attrs and 0:
			print "\nMyDocument attrs parameters:"
			for key in attrs.keys():
				print "\t%s: %s" % (key, attrs[key])
			print ""
				
		if attrs.has_key ("title"):
			self.mytitle = attrs["title"]
			del attrs["title"]
		
		if attrs.has_key ("stylesheet"):
			## self.style is added to head automatically by Document
			# self.style = LINK (rel="stylesheet", type="text/css", href=attrs["stylesheet"])
			self.stylesheet = attrs['stylesheet']
			del attrs["stylesheet"]
		
		if attrs.has_key ("javascript"):
			# self.javascript must added manually after call to Document.__init__
			self.javascript = attrs["javascript"]
			del attrs["javascript"]	
		
		Document.__init__ (self, *content, **attrs)
		## if hasattr (self, "javascript"):self.head.append(self.javascript)
		if hasattr (self, "javascript"):self.addJavascript(self.javascript)
		if hasattr (self, "stylesheet"):self.addStylesheet(self.stylesheet)

		if hasattr (self, "mytitle"):
			self.head.append (TITLE (self.mytitle))
			# self.body.content.insert (0, H1 (self.mytitle))
	
	def addJavascript (self, javacript_src):
		if type (javacript_src) == type (""):
			javacript_src = [javacript_src, ]
		for src in javacript_src:
			self.head.append (SCRIPT (TYPE="text/javascript", src=src))
	
	def addStylesheet (self, stylesheet_ref):
		if type (stylesheet_ref) == type (""):
			stylesheet_ref = [stylesheet_ref, ]
		for src in stylesheet_ref:
			# self.head.append (SCRIPT (TYPE="text/javascript", src=src))
			self.head.append (LINK (rel="stylesheet", type="text/css", href=src))
			
	def writeto(self, path, indent=0, perlevel=2):
		f = open (path, 'w')
		f.write (self.__str__())
		f.close()
	
	
if __name__ == "__main__":
	# <link rel='stylesheet' type='text/css' href='styles.css'>
	stylesheet = "styles.css"
	
	# <script language="JavaScript" src="javascript.js" />
	javascript = "javascript.js"
	
	
	doc = HtmlDocument (stylesheet=stylesheet, javascript=javascript)
	print doc
