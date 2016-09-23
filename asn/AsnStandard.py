import string
from HyperText.HTML40 import *
from util import *

class AsnStandard:

	encoding = 'utf-8' # 'iso-8859-1'

	def __init__ (self, id, children, parent, description, gradeRange=None):
		self.id = id
		self.children = children
		## self.children.sort()
		self.parent = parent
		self.description = description
		self.gradeRange = gradeRange
		self.level = None
		self.numId = getNumId (self.id)

	def toString (self):
		s=[];add = s.append
		add ("\nid: " + self.id)
		add ("\t parent: %s" % self.parent)
		add ("\t level: %d" % self.level)
		add ("\t children: \n\t\t%s" % string.join (self.children, "\n\t\t"))
		add ("\t description: %s" % self.description)	
		add ("\t gradeRange: %s" % self.gradeRange)
		return string.join (s, "\n").encode(self.encoding, 'replace')

class AsnStandardHtml (AsnStandard):

	def _collapseWidget (self, id):
		title = "click to hide/show children; shift-click to hide/show siblings"
		return  IMG (src="images/opened.gif", title=title, klass="widget")

	def _leafWidget (self, id):
		title = "click to go to parent standard"
		return IMG (src="images/leaf.gif", title=title, klass="widget")

	def _idLink (self):
		onclick = "alert ('%s');return false" % self.id
		# text = "[ %s ]" % Href (self.id, self.numId, onclick=onclick)
		text = "[ %s ]" % Href (self.id, self.numId) # no click handler
		return SPAN (text, klass="std-id")

	def _idTag (self, id=None):
		if id is None:
			id = self.id
		tag = "[&nbsp;%s&nbsp;]" % id
		return SPAN (tag,  klass="std-id")
		
	def getStats (self):
		# show gradeRange
		stats = DIV (klass="std-stats", id=self.numId+"_stats")
		stats.append (DIV ("std-level: %s" % self.level))
		stats.append (DIV ("gradeRange: %s" % self.gradeRange))
		
		return stats
		
	def _gradeRange (self):
		# text = "gradeRange: %s" % self.gradeRange
		text = "%s" % self.gradeRange
		return SPAN (text, klass="std-id")
	
	def toHtml (self):
		"""
		 represent this standards item as html
		"""
			
		if self.level is None:
			raise "unable to produce html: level is not initialized"
			
		id = self.id
		

		std = DIV (klass="node", id=self.numId)
		head = DIV (klass="node-head")
		std.append (head)
		
		if self.children:
			widget = self._collapseWidget (self.numId)
		else:
			widget = self._leafWidget (self.numId)
			
		# std.append (A (widget, name=numId))
		head.append (DIV (widget, klass="node-control"))
		
		text = self.description.encode("utf8", "replace")
		
		# show level for debugging purposes
		##text = "(%d) %s" % (self.level, text)
		
		# show id following standard text
		## text = "%s %s" % (text, self._idTag(numId))
		
		# show id LINK  following standard text
		# text = "%s %s" % (text, self._idLink())
		
		# show gradeRange before id link
		text = "%s %s %s" % (text, self._idLink(), self._gradeRange())
		
		head.append (DIV (text, klass="node-text"))

		return std
		

