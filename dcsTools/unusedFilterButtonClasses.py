import sys, string
sys.path.append ("/Users/ostwald/devel/python-lib")

from logTools.CatalinaLogTool import CatalinaLogTool, Filter, DateFilter
from logTools.tkLogTool import TkLogTool, normal_font, header_font
from logTools.LogToolWidget import LogToolWidget
from logTools.utils import normal_font, header_font

from Tkinter import *

class FilterButton (Button, LogToolWidget):
	# button state info could be stashed here, for
	# callback handler to use ...
	def __init__ (self, parent, text=None, command=None):
		func = (lambda button=self, func=command: func(button))
		Button.__init__(self, parent, text=text, command=func)

	def makeFilter (self):
		return "1 == 1"

class ToggleButton (Button, LogToolWidget):
	"""
	a button that highlights itself when "on"
	"""
	def __init__ (self, parent, text=None, state=0):
		Button.__init__(self, parent, text=text, command=self.toggle)
		self.state = state
		self.highlight()

	def highlight (self):
		if self.state == 0:
			self.config (bg="green")
		else:
			self.config (bg="red")
			
	def toggle (self):
		if self.state == 0:
			# print "toggling to ON"
			self.state = 1
		else:
			# print "toggling to OFF"
			self.state = 0
		self.highlight()
			
	def makeFilter (self):
		return "make filter not implemented"

class StatusFilterButton (ToggleButton):
	def __init__ (self, parent, text="StatusFilterButton", state=0):
		ToggleButton.__init__ (self, parent, text=text, state=state)
	
	def makeFilter (self):
		# print "StatusFilterButton: makeFilter: state is %d" % self.state
		if self.state == 1:
			return "request.isStatusEvent()"
