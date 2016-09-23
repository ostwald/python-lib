# define a name:callback demos table
"""
todo: 
	Filter control panel should:
		- provide controls for each type of filter to be created:
			Status
			DateRange
			OutOfMemory
			StackOverFlow
			...
		- update button creates a list of filters and calls method
		in tkLogTool to update filters and display
	
			- this can be prototyped using the "quit" method ...
"""

import sys, string, time
sys.path.append ("/Users/ostwald/devel/python-lib")

from logTools.utils import TimeTool, secsToLogTime, normal_font, header_font
from logTools.CatalinaLogTool import CatalinaLogTool, Filter, DateFilter
from logTools.LogToolWidget import LogToolWidget

from DateFilterWidget import ToggledDateWidget

from Tkinter import *
from tkFileDialog	import askopenfilename		  # get standard dialogs
from tkColorChooser import askcolor				  # they live in Lib/lib-tk
from tkMessageBox	import askquestion, showerror
from tkSimpleDialog import askfloat

"""
just one button
- when clicked, creates a filter

- capture window close and create FilterList
"""

def log (s):
	sys.stdout.write ("FilterButtons: " + s + "\n")

class FilterFrame (Frame, LogToolWidget):

	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.config (bd=5, bg="#ccccff")
		self.pack (side=TOP, fill=X)
		self.filters = []
		self.makewidgets()
		
		
	def makewidgets (self):
		w = StatusCheckbutton (self, text="StatusCheckbutton")
		w.pack(side=TOP, fill=X)
		s = SessionIdWidget (self)
		s.pack(side=TOP, fill=X)
		dfw = DateFilterWidget (self, text="DateFilterWidget")
		dfw.pack()
		Button (self, text="update", command=self.update).pack (side=TOP)
		
		
	def quit(self):
		print "quiting"

		self.filters = self.buildFilterList()
		self.showFilters()
		Frame.quit(self)

	def buildFilterList (self):
		filters = []
		try:
			for child in self.children.values():
				# print child.__class__.__name__
				if hasattr (child, "makeFilter"):
					print "\t%s\n\t\tfilter: %s\n" % (child.__class__.__name__, child.makeFilter())
					filter = child.makeFilter()
					if filter:
						filters.append (filter)
		except:
			print sys.exc_info()[0], sys.exc_info()[1]
			print "FilterFrame.getFilterList bailing ..."
		return filters
			
	def showFilters (self):
		s=[];add=s.append
		if self.filters:
			for f in self.filters: add(str(f))
		else:
			add ("No Filters defined")
		return string.join (s, "\n\t")
	
	def update (self):
		log ("\n%s\nFilterFrame UPDATE" % ("-"*50))
		self.filters = self.buildFilterList()
		self.showFilters()
		logTool = self.getLogToolFrame ()
		if logTool:
			logTool.applyFilters (self.filters)
		

class StatusCheckbutton (Checkbutton):
	def __init__ (self, parent, text="status", **kw):
		self.var = IntVar()
		Checkbutton.__init__ (self, parent, text=text, variable=self.var, command=self.cb)
		self.config (bg=parent['bg'], anchor=W)
		
	def makeFilter (self):
		if self.var.get():
			return Filter ("isStatusEvent()")

	def cb (self):
		# print "variable is", self.var.get()
		pass


class ToggledEntry (Frame):
	"""
	default value provided for date fields
	"""
	def __init__ (self, parent, text="ToggledEntry", state=0):
		self.default = "toggledEntry default"
		Frame.__init__ (self, parent)
		self.config (bd=3, bg=parent['bg'])
		self.var = IntVar()
		self.var.set (state)
		toggle = Checkbutton (self, variable=self.var, command=self.cb_t)
		toggle.config (anchor=W, bg=self['bg'])
		toggle.pack (side=LEFT, fill=Y)
		Label (self, text=text, anchor=W, bg=self['bg'] ).pack (side=TOP, fill=X)
		self.textvar = StringVar()
		entry = Entry (self, textvariable=self.textvar, bg="white")
		entry.pack (side=TOP, fill=X)

	def cb_t (self):
		# print "toggledEntry variable is", self.var.get()
		pass

	def cb_e (self):
		## print "toggledEntryentry is", self.textvar.get()
		pass

	def setEntry (self, value):
		self.textvar.set (value)
		
	def getEntry (self):
		if self.var.get():
			return self.textvar.get() or self.default
		
	def makeFilter (self):
		return None

class SessionIdWidget (ToggledEntry):
	def __init__ (self, parent):
		ToggledEntry.__init__ (self, parent, text="Session ID")

	def makeFilter (self):
		sessionId = self.getEntry()
		if sessionId:
			return Filter ("sessionId", val=sessionId)

class DateFilterWidget (Frame):
	def __init__ (self, parent, text=None):
		Frame.__init__(self, parent)
		self.config (bd=2, bg="#ffcccc", relief=SUNKEN)
		
		Label (self, text="Date Filter", font=header_font, anchor=W, bg=self['bg']).pack (side=TOP, fill=X)
		
		self.since_widget = ToggledDateWidget (self, "Since", toggle_state=0)
		self.since_widget.config (bg=self['bg'])
		self.since_widget.pack(side=TOP, fill=X)
		self.before_widget = ToggledDateWidget (self, "Before", toggle_state=0)
		self.before_widget.config (bg=self['bg'])
		self.before_widget.pack(side=TOP, fill=X)
		
	def makeFilter (self):
		since_time = self.since_widget.getDate() or secsToLogTime (0)
		before_time = self.before_widget.getDate() or secsToLogTime (time.time())
		# print "since_widget: %s, before_widget: %s" % (since_time, before_time)
		return DateFilter (since_time, before_time)
			
def makeFilterFrame ():		
	root = Tk()
	filterFrame = FilterFrame()
	root.protocol("WM_DELETE_WINDOW", filterFrame.quit)
	root.mainloop()
	
if __name__ == "__main__":
	makeFilterFrame()



