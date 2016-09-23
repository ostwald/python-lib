# define a name:callback demos table

import os,sys

if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from string import find
from UserDict import UserDict
from instanceWalker import InstanceWalker, DcsInstance
from logTools.LogToolWidget import LogToolWidget
from Tkinter import *
from tkFileDialog   import askopenfilename        # get standard dialogs
from tkColorChooser import askcolor               # they live in Lib/lib-tk
from tkMessageBox   import askquestion, showerror
from tkSimpleDialog import askfloat


mj_tomcats = {"mj devel" : "/Library/Java/Extensions/tomcat/tomcat",
			  "tomcat-test" : "/Library/Java/Extensions/tomcat/tomcat-test",
			  "anisart-tomcat" : "/Library/Java/Extensions/tomcat/anisart-tomcat"}

taos_tomcats = {
	"tomcat/tomcat" : "/Library/Java/Extensions/tomcat/jakarta-tomcat-5.0.16",
	"ani-tomcat" : "/Library/Java/Extensions/tomcat/tomcat-ani"
}

tremor_tomcats = {
	"devel" : "L:/ostwald/tomcat/tomcat",
	"test" : "L:/ostwald/tomcat/tomcat-test",
	"clean" : "L:/ostwald/tomcat/tomcat-clean",
	"preview" : "L:/preview/ostwald/tomcat/tomcat-preview"
}

def log (s):
	sys.stdout.write ("InstanceButtons: " + s + "\n")

default_tomcat_map = tremor_tomcats

class InstanceList (UserDict):
	"""
	a list of DcsInstance instances, keyed by path
	"""

	def __init__ (self):
		UserDict.__init__ (self)
		self._load()
		self.instances = self._get_sorted_values()
	
	def _load (self):
		host = os.getenv ("HOST")
		platform = sys.platform
		log ("\thost: %s\n\tplatform %s" % (os.getenv ("HOST"), sys.platform))
		self.clear()
		if host and host.find ("bolide")!= -1:
			bolide_instance_path = "/export/services/dcs/dcs.dlese.org/tomcat"
			walker = InstanceWalker (bolide_instance_path)
			for instance in walker.instances:
				self._put (instance)
				return
		if platform == 'darwin':
			tomcat_map = mj_tomcats
		else:
			tomcat_map = default_tomcat_map
			
		for key in tomcat_map.keys():
			print key
			self._put (DcsInstance (tomcat_map[key], key))
				

	def _put (self, instance):
		self[instance.path] = instance

	def getInstance (self, path):
		if self.has_key (path):
			return self[path]

	def _get_sorted_values (self):
		values = self.values()
		values.sort (lambda a, b: cmp(a.displayname, b.displayname))
		return values

class InstanceButton (Button, LogToolWidget):
	# button state info could be stashed here, for
	# callback handler to use ...
	def __init__ (self, parent, instance, **kw):
		self.instance = instance
		self.text = instance.displayname
		self.path = instance.path
		Button.__init__(self, parent, kw, text=self.text, command=self.onSetInstance)

	def onSetInstance (self):
		"""
		handler for instance button
		update the logTool with log from selected instance
		"""
		log ("onSetInstance: " + self.text)

		logToolFrame = self.getLogToolFrame()
		if logToolFrame:
			logToolFrame.setCurrentInstance (self.instance)
		else:
			log ("could not find LogToolFrame - bailing")

	## 	logFilePath = self.path + "/logs/catalina.out"
## 		logToolFrame.pathLabel.config (text=logFilePath)
## 		logToolFrame.logTool.changePath(logFilePath)
## 		logToolFrame.update_log_text()




if __name__ == "__main__":
	root = Tk()
	for instance in InstanceList().instances:
		InstanceButton (root, instance, padx=10).pack(side=LEFT)
	root.mainloop()
