# define a name:callback demos table

import os,sys

if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from string import find
from Tkinter import *
from tkFileDialog   import askopenfilename        # get standard dialogs
from tkColorChooser import askcolor               # they live in Lib/lib-tk
from tkMessageBox   import askquestion, showerror
from tkSimpleDialog import askfloat


class LogToolWidget (Widget):

	"""
	provides a method to access the logToolFrame
	"""
	
	def getLogToolFrame (self):
		"""
		search up the tk master chain looking for the TkLogTool
		return None if not found
		"""
		obj = self
		while obj.master is not None:
			obj = obj.master
			class_name = obj.__class__.__name__
			## print "obj.__class__: %s" % class_name
			if find (class_name, "TkLogTool") != -1:
				return obj
