# define a name:callback demos table

import sys
sys.path.append ("/Users/ostwald/devel/python-lib")

from logTools.CatalinaLogTool import CatalinaLogTool, Filter, DateFilter
from logTools.tkLogTool import TkLogTool
from InstanceButtons import InstanceList

from Tkinter import *
from tkFileDialog   import askopenfilename        # get standard dialogs
from tkColorChooser import askcolor               # they live in Lib/lib-tk
from tkMessageBox   import askquestion, showerror
from tkSimpleDialog import askfloat

demos = {
    'Open':  askopenfilename, 
    'Color': askcolor,
    'Query': lambda: askquestion('Warning', 'You typed "rm *"\nConfirm?'),
    'Error': lambda: showerror('Error!', "He's dead, Jim"),
    'Input': lambda: askfloat('Entry', 'Enter credit card number')
}



class DashButton (Button):
	# button state info could be stashed here, for
	# callback handler to use ...
	def __init__ (self, parent, text=None, command=None):
		func = (lambda button=self, func=command: func(button))
		Button.__init__(self, parent, text=text, command=func)

	def getDashBoard (self):
		return self.master

	def getRoot (self):
		obj = self
		while obj.master is not None:
			obj = obj.master
		return obj

## should be written to be called with an instance of DashButton,
## so state can be accessed
def onLogTool (button):
	## state can also be passed as param with run-time expression,
	## such as lambda?
	print "log tool"

def onChooseInstance (button):
	print "onChooseInstance"

def closeTool (win, dash):
	print ("closing tool");
	dash.focus()
	win.destroy()
	
def onStatusEvents (button):
	## state can also be passed as param with run-time expression,
	## such as lambda?

	print "onStatusEvents"
	path = "logTools/catalina.out.sample"
	root = button.getRoot()
	win = Toplevel (button.getRoot())
	win.title ("Catalina Log Tool")
	quit = (lambda win=win, dashboard=button.getDashBoard(): closeTool (win, dashboard))
	win.protocol("WM_DELETE_WINDOW", quit)

	# define some filters
	filters = []
	t1 = "Feb 2, 2006 9:42:32 AM"
	t2 = "Feb 10, 2006 9:42:32 AM"

	filters.append (DateFilter (t1,t2))
	filters.append (Filter ("isStatusEvent()"))
	tkLogTool = TkLogTool (win, InstanceList(), filters=filters)

general_buttons = {
	# "log tool":onLogTool
	"status events":onStatusEvents
}

instance_buttons = {
	"choose instance":onChooseInstance,
}
