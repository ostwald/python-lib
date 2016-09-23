import sys, string
sys.path.append ("/Users/ostwald/devel/python-lib")

import time

from logTools.utils import TimeTool, normal_font, header_font
from logTools.CatalinaLogTool import CatalinaLogTool, Filter, DateFilter

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

class ToggledDateWidget (Frame):
	def __init__ (self, parent, label="ToggleDateWidget", toggle_state=0):
		self.toggle_state = toggle_state
		self.label = label
		Frame.__init__ (self, parent)
		self.config (bd=3, bg=parent['bg'])
		self.makewidgets ()
		
	def makewidgets (self):
		self.var = IntVar()
		self.var.set (self.toggle_state)
		toggle = Checkbutton (self, variable=self.var, command=self.cb_t)
		toggle.config (anchor=W, bg=self['bg'])
		toggle.pack (side=LEFT, fill=Y)
		
		Label (self, text=self.label, anchor=W, bg=self['bg'] ).pack (side=TOP, fill=X)
		
		self.datewidget = DateWidget (self)
		self.datewidget.pack ()

	def cb_t (self):
		## print "toggledEntry variable is", self.var.get()
		pass

	def getDate (self):
		return self.var.get() and self.datewidget.getDate()
		
	def quit (self):
		print self.getDate ()
		Frame.quit (self)
			
class DateWidget (Frame):
	def __init__ (self, parent):
		Frame.__init__ (self, parent)
		self.timetool = TimeTool(time.time())
		self.makewidgets ()
		
	def makewidgets (self):
		MonthWidget (self).pack(side=LEFT)
		self.getDivider ("/")
		DayWidget (self).pack(side=LEFT)
		self.getDivider ("/")
		YearWidget (self).pack(side=LEFT)
		self.getDivider ("  ")
		HourWidget (self).pack(side=LEFT)
		self.getDivider (":")
		MinuteWidget (self).pack(side=LEFT)
		self.getDivider (":")
		SecondWidget (self).pack(side=LEFT)
		
	def getDivider (self, text):
		Label (self, text=text, anchor=S).pack(side=LEFT, fill=Y)
		
	def getDate (self):
		for w in self.children.values():
			try:
				val = int (w.getValue())
				# print "%s: %d" % (w.tm_id, val)
				self.timetool[w.tm_id] = val
			except:
				# print "%s: %s (%s)" % (w.tm_id, sys.exc_info()[0], sys.exc_info()[1])
				pass
		return self.timetool.logTime()
		
class DateEntryWidget (Frame):
	def __init__ (self, parent, label=None, tm_id=None, valrange=range(1), maxlength=2):
		self.tm_id = tm_id
		self.valrange = valrange
		self.default = self.valrange[0]
		self.maxlength = maxlength
		self.value = parent.timetool[tm_id]
		Frame.__init__ (self, parent)
		
		if label:
			Label (self, text=label, anchor=W).pack (side=TOP, fill=X)
		
		self.var = StringVar()
		self.var.set (self.value);
		self.entry = Entry (self, width=self.maxlength, justify=RIGHT, textvariable=self.var)
		self.var.trace('w', self._entry_callback)
		self.entry.pack(side=TOP)
		
	def setval (self, val):
		try:
			v = int(val)
		except ValueError:
			return
		self.var.set(val)
		
	def _entry_callback(self, *dummy):
		value = self.var.get()
		newvalue = self._validate_entry(value)
		if newvalue is None:
			self.var.set(self.value)
		elif newvalue != value:
			self.value = newvalue
			self.var.set(newvalue)
		else:
			self.value = value
			
	def _validate_entry (self, value):
		if value == "": return value
		try:
			v = int (value)
		except ValueError:
			print "InvalidValue", "(%s: %s)" % (sys.exc_type, sys.exc_value)
			return None
		if self.maxlength:
			value = value[:self.maxlength]
			v = int(value)
			if len(value) == self.maxlength and v not in self.valrange:
				print "InvalidValue", "'%d' is out of range" % v
				return None
		return value
		
	def getValue (self):
		## print "getValue (%s): self.value: %s" % (self.tm_id, self.value)
		return self.value or self.valrange[0]
		
class DayWidget (DateEntryWidget):
	def __init__ (self, parent):
		label = "day"
		tm_id="tm_mday"
		valrange = range (1,32)

		DateEntryWidget.__init__ (self, parent, label=label, tm_id=tm_id, valrange=valrange)

class MonthWidget (DateEntryWidget):
	def __init__ (self, parent):
		label = "mon"
		tm_id = "tm_mon"
		valrange = range (1,13)
		DateEntryWidget.__init__ (self, parent, label=label, tm_id=tm_id, valrange=valrange)
	
class YearWidget (DateEntryWidget):
	def __init__ (self, parent):
		label = "yr"
		tm_id = "tm_year"
		valrange = range (2000,2010)
		maxlength = 4
		DateEntryWidget.__init__ (self, parent, label=label, tm_id=tm_id, valrange=valrange, maxlength=maxlength)
		
class HourWidget (DateEntryWidget):
	def __init__ (self, parent):
		label = "hr"
		tm_id = "tm_hour"
		valrange = range (24)
		DateEntryWidget.__init__ (self, parent, label=label, tm_id=tm_id, valrange=valrange)
		
class MinuteWidget (DateEntryWidget):
	def __init__ (self, parent):
		label = "min"
		tm_id = "tm_min"
		valrange = range (60)
		DateEntryWidget.__init__ (self, parent, label=label, tm_id=tm_id, valrange=valrange)
		
class SecondWidget (DateEntryWidget):
	def __init__ (self, parent):
		label = "sec"
		tm_id = "tm_sec"
		valrange = range (60)
		DateEntryWidget.__init__ (self, parent, label=label, tm_id=tm_id, valrange=valrange)
		
if __name__ == "__main__":
	## makeFilterFrame()
	root = Tk ()
	dw = ToggleDateWidget (root)
	dw.pack()
	root.protocol("WM_DELETE_WINDOW", dw.quit)
	root.mainloop ()


