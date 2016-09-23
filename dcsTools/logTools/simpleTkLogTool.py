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

from dcsTools.InstanceButtons import InstanceButton, get_instances

def log (s):
	sys.stdout.write ("INFO: " + s + "\n")

class TkLogTool (Frame):

	"""
	creates a frame holding a logTool
	"""
	
	def __init__ (self, parent=None, path=None, filters=[]):
		Frame.__init__ (self, parent)
		self.pack(expand=YES, fill=BOTH)

		## state variables
		self.header_font = tkFont.Font(family='arial', size=12, weight=tkFont.BOLD)
		self.normal_font = tkFont.Font(family='helvetica', size=10)
		
		self.logTool = CatalinaLogTool (path, filters)
		self.pathLabel = None
		self.log_text = None
		self.filter_text = None
		self.current_instance = None

		## initialization
		self.makewidgets()

		
##		self.mainloop()

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
			else:
				log ("file does not exist at " + newPath)

	def makewidgets (self):
		host = os.getenv("HOST")
		print "host: ", host
		if (host == "bolide"):
			instanceFrame = Frame (self, bg="yellow")
			Label (instanceFrame, text="instances go here").pack()
			instanceFrame.pack (side=TOP, expand=NO, fill=X)

		pathFrame = Frame (self, bg='black' )
		Label (pathFrame, text="path ").pack (side=LEFT, expand=NO)

		browse = Button (pathFrame, text="browse", command=self.onFileBrowse, bd=5)
		browse.pack (side=RIGHT, fill=X)	
		
		self.pathLabel = Label (pathFrame, text=self.logTool.path, background="black", fg="white")
		self.pathLabel.pack (side=LEFT)
		pathFrame.pack (side=TOP, expand=NO, fill=X)

		self.getInstanceButtons ()

		self.getFilterFrame ()

		statusFrame = Frame (self, height=20, bg="gray")
		statusFrame.pack (side=BOTTOM, fill=X)

		self.log_text = ScrolledText(self)
		self.update_log_text()

	def updateFilterText (self):
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

	def getInstanceButtons (self):
		instances = get_instances()
		if not instances: return
		self.instanceFrame = Frame (self, bg="gray", bd="5")
		for instance in instances.keys():
			InstanceButton (self.instanceFrame, instance, instances[instance]).pack(side=LEFT)
		self.instanceFrame.pack (side=TOP, fill=X)

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

		
class ScrolledText(Frame):
	def __init__(self, parent=None, text='', file=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)				 # make me expandable
		self.makewidgets()
		self.settext(text, file)

	def makewidgets(self):
		sbar = Scrollbar(self)
		text = Text(self, relief=SUNKEN)
		sbar.config(command=text.yview)					 # xlink sbar and text
		text.config(yscrollcommand=sbar.set)			 # move one moves other
		sbar.pack(side=RIGHT, fill=Y)					 # pack first=clip last
		text.pack(side=LEFT, expand=YES, fill=BOTH)		 # text clipped first
		self.text = text
		
	def settext(self, text='', file=None):
		debug = text
		if len (debug) > 20:
			debug = debug[:20]+" ..."
		log ("settext: " + debug)
		if file: 
			text = open(file, 'r').read()
		self.text.delete('1.0', END)					 # delete current text
		self.text.insert('1.0', text)					 # add at line 1, col 0
		self.text.mark_set(INSERT, '1.0')				 # set insert cursor
		self.text.focus()								 # save user a click

	def gettext(self):									 # returns a string
		return self.text.get('1.0', END+'-1c')			 # first through last


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
	tkLogTool = TkLogTool (root, path=path, filters=filters)
	root.mainloop()
	
if __name__ == '__main__':

	## old_tester()
	newTester()
