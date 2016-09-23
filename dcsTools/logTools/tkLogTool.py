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
from dcsTools.FilterButtons import FilterFrame
from utils import normal_font, header_font

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
		self.instanceList = instanceList
		self.current_instance = current_instance
		logPath = None
		if self.current_instance:
			logPath = current_instance.path
		self.logTool = CatalinaLogTool (logPath, filters)
		self.log_text = None

		## initialization
		self.makewidgets()


	def onKeyPress (self, event):
		"""
		786545 is cmd-q
		852087 is cmd-w
		"""
		# print "got key press:", event.keycode
		if event.keycode == 786545 or event.keycode == 852087:
			self.quit()

	def setCurrentInstance (self, instance):

		self.current_instance = instance
		logFilePath = instance.path + "/logs/catalina.out"
		self.pathFrame.update (logFilePath)
		self.logTool.changePath(logFilePath)
		self.instanceButtonsFrame.update()
		self.update_log_text()

	def applyFilters (self, filterList=None):
		if filterList:
			self.logTool.applyFilters (filterList)
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
				self.pathFrame.update (text=newPath)
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
		toolLabel = Label (self, text="Catalina Log Tool", font=header_font,
						   bg="#ffffcc", pady=3)
		toolLabel.pack(side=TOP, fill=X)


		self.pathFrame = PathFrame(self)

		self.instanceButtonsFrame = InstanceButtonsFrame(self)

		self.filterFrame = FilterFrame (self)

		self.statusText = StatusText (self)

		self.log_text = ScrolledText(self)
		self.log_text.text.config (bg="white")
		self.update_log_text()



	def quit (self, event=None):
		print "good-bye"
		self.master.quit()

	def update_log_text (self):
		log ("update_log_text")
		logReport = "Please choose an instance"
		if self.logTool.path:
			logReport = self.logTool.report()

		if self.log_text is not None:
			self.log_text.settext (text=logReport)
		else:
			print "update_log_text: self.logText is None"


class StatusText (Label):
	def __init__ (self, parent, text=""):
		Label.__init__ (self, parent, text=text, bg="gray", anchor=W)
		self.pack (side=BOTTOM, fill=X)

	def update (self, text):
		self.config (text=text)

class FilterFrameOLD (Frame):
	
	def __init__ (self, parent):

		Frame.__init__ (self, parent, height=20)
		self.pack (side=TOP, fill=X)
		Label (self, text="Filters", font=header_font, anchor=W).pack (side=TOP, fill=X)
		self.filter_text = Label (self, font=normal_font)
		self.update()
		self.filter_text.pack (side=LEFT, fill=X)

	def update (self):
		"""
		update the test that describes the current filters
		"""
		filters = self.master.logTool.filters
		if self.filter_text:
			flist = map (str, filters)
			self.filter_text.config (text=string.join (flist, '\n'))


class InstanceButtonsFrame (Frame):

	def __init__ (self, parent):
		log ("getInstanceButtons")

		instances = []
		if parent.instanceList:
			instances = parent.instanceList.instances
		if not instances:
			print "no instances found"
			return
		Frame.__init__ (self, parent, bg="gray", bd="5")
		self.pack (side=TOP, fill=X)
		for instance in instances:
			print ("adding button for %s" % instance.displayname)
			InstanceButton (self, instance).pack(side=LEFT)
		self.update ()

	def update (self):
		"""
		highlight the button corresponding to the current_instance
		"""
		for c in self.children.values():
			if isinstance (c, InstanceButton):
				if c.instance == self.master.current_instance:
					c.config (bg="yellow")
				else:
					c.config (bg="white")



class PathFrame (Frame):
	
	def __init__ (self, parent):
		Frame.__init__ (self, parent, bg='black')
		labelConfig = {"background":"black", "fg":"white", "font":normal_font}
		promptLabel = Label (self, text="path: ")
		promptLabel.config (labelConfig)
		promptLabel.pack (side=LEFT, expand=NO)
		browse = Button (self, text="browse", command=parent.onFileBrowse, bd=5)
		browse.pack (side=RIGHT, fill=X)

		self.pathLabel = Label (self, text=parent.logTool.path)# , background="black", fg="white")
		self.pathLabel.config (labelConfig)
		self.pathLabel.pack (side=LEFT)
		self.pack (side=TOP, expand=NO, fill=X)

	def update (self, text):
		self.pathLabel.config (text=text)

		
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
	# filters.append (Filter ("isStatusEvent()"))
	instanceList = InstanceList()
	print "instances"
	for i in instanceList.instances:
		print "\t%s (%s)" % (i.displayname, i.path)
	tkLogTool = TkLogTool (root, instanceList, filters=filters)
	root.bind ('<Control-q>', tkLogTool.quit)
	root.bind ('<KeyPress>', tkLogTool.onKeyPress)
	root.mainloop()
	
if __name__ == '__main__':

	## old_tester()
	newTester()
