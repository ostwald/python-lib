# displays info from CatalinaLogTool into a tk window

print 'tk Log Tool'


import os, sys, string

print "\thost: %s\n\tplatform %s" % (os.getenv ("HOST"), sys.platform)

if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from Tkinter import *
import tkFont
from tkFileDialog   import askopenfilename
from CatalinaLogTool import CatalinaLogTool, Filter, DateFilter
from gui.quitter import Quitter
from gui.ScrolledText import ScrolledText

from dcsTools.InstanceButtons import InstanceButton, InstanceList

def log (s):
	sys.stdout.write ("tkLogTool: " + s + "\n")

class TkLogTool (Frame):

	"""
	creates a frame holding a logTool
	"""
	
	def __init__ (self, parent=None, instanceList=None, current_instance=None, filters=[]):
		Frame.__init__ (self, parent)
		self.pack(expand=YES, fill=BOTH)

		## state variables
		self.header_font = tkFont.Font(family='arial', size=12, weight=tkFont.BOLD)
		self.normal_font = tkFont.Font(family='helvetica', size=10)

		self.instanceList = instanceList
		logPath = None
		if current_instance:
			logPath = current_instance.path
		self.logTool = CatalinaLogTool (logPath, filters)
		self.pathLabel = None
		self.log_text = None
		self.filter_text = None
		self.current_instance = current_instance

		## initialization
		self.makewidgets()

		
##		self.mainloop()

	def setCurrentInstance (self, instance):
		self.current_instance = instance
		logFilePath = instance.path + "/logs/catalina.out"
		self.pathLabel.config (text=logFilePath)
		self.logTool.changePath(logFilePath)
		self.updateInstanceButtons()
		self.update_log_text()

	def onFileBrowse (self):
		print "onFileBrowse"

		_path = self.logTool.path

## 		initialDir = os.getcwd()
## 		if os.path.exists (_path):
## 			dir = os.path.dirname (_path)
## 		newPath = askopenfilename(parent=self, title="choose new log file",
## 								  defaultextension="out", initialdir=dir)
		newPath = askopenfilename(parent=self, title="choose new log file")
			
		if newPath != _path and \
		   newPath is not None:
			if os.path.exists (newPath):
				self.pathLabel.config (text=newPath)
				self.logTool.changePath(newPath)
				self.update_log_text()
				self.current_instance = None
				self.updateInstanceButtons()
			else:
				log ("file does not exist at " + newPath)

	def makewidgets (self):
		host = os.getenv("HOST")
		print "host: ", host

#		instanceFrame = Frame (self, bg="yellow")
		toolLabel = Label (self, text="Catalina Log Tool", font=self.header_font,
						   bg="#ffffcc", pady=3)
		toolLabel.pack(side=TOP, fill=X)
#		instanceFrame.pack (side=TOP, expand=NO, fill=X)

		self.getPathFrame ()

		self.getInstanceButtonFrame ()

		self.getFilterFrame ()

		statusFrame = Frame (self, height=20, bg="gray")
		statusFrame.pack (side=BOTTOM, fill=X)

		self.log_text = ScrolledText(self)
		self.log_text.text.config (bg="white")
		self.update_log_text()

	def getPathFrame (self):
		pathFrame = Frame (self, bg='black' )
		labelConfig = {"background":"black", "fg":"white"}
		promptLabel = Label (pathFrame, text="path: ")
		promptLabel.config (labelConfig)
		promptLabel.pack (side=LEFT, expand=NO)
		browse = Button (pathFrame, text="browse", command=self.onFileBrowse, bd=5)
		browse.pack (side=RIGHT, fill=X)

		self.pathLabel = Label (pathFrame, text=self.logTool.path)# , background="black", fg="white")
		self.pathLabel.config (labelConfig)
		self.pathLabel.pack (side=LEFT)
		pathFrame.pack (side=TOP, expand=NO, fill=X)

	def updateFilterText (self):
		"""
		update the test that describes the current filters
		"""
		if self.filter_text:
			flist = map (str, self.logTool.filters)
			self.filter_text.config (text=string.join (flist, '\n'))

	def getFilterFrame (self):
		filterFrame = Frame (self, height=20)
		filterFrame.pack (side=TOP, fill=X)
		Label (filterFrame, text="Filters", font=self.header_font, anchor=W).pack (side=TOP, fill=X)
		self.filter_text = Label (filterFrame, font=self.normal_font)
		self.updateFilterText()
		self.filter_text.pack (side=LEFT, fill=X)

	def updateInstanceButtons (self):

		if not (self.instanceFrame and self.instanceList): return
		
		for c in self.instanceFrame.children.values():
			if isinstance (c, InstanceButton):
				if c.instance == self.current_instance:
					c.config (bg="yellow")
				else:
					c.config (bg="white")

	def getInstanceButtonFrame (self):
		log ("getInstanceButtons")
		if not self.instanceList.instances:
			print "no instances found"
			return
		self.instanceFrame = Frame (self, bg="gray", bd="5")
		self.instanceFrame.pack (side=TOP, fill=X)
		for instance in self.instanceList.instances:
			print ("adding button for %s" % instance.displayname)
			InstanceButton (self.instanceFrame, instance).pack(side=LEFT)
		self.updateInstanceButtons ()

	def quit (self):
		print "good-bye"

	def update_log_text (self):
		log ("update_log_text")
		logReport = "Please choose an instance"
		if self.logTool.path:
			logReport = self.logTool.report()

		if self.log_text is not None:
			self.log_text.settext (text=logReport)
		else:
			print "update_log_text: self.logText is None"

		
def newTester ():

	## path = "catalina.out.sample"
	path = None
	root = Tk()
	root.title ("Catalina Log Tool")


	# define some filters
	filters = []
	t1 = "Feb 2, 2006 9:42:32 AM"
	t2 = "Feb 10, 2006 9:42:32 AM"

	## filters.append (DateFilter (t1,t2))
	filters.append (Filter ("isStatusEvent()"))
	instanceList = InstanceList()
	print "instances"
	for i in instanceList.instances:
		print "\t%s (%s)" % (i.displayname, i.path)
	tkLogTool = TkLogTool (root, instanceList, filters=filters)
	root.mainloop()
	
if __name__ == '__main__':

	## old_tester()
	newTester()
