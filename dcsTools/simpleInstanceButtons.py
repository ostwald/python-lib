# define a name:callback demos table

import os,sys

if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from string import find
from instanceWalker import InstanceWalker
from Tkinter import *
from tkFileDialog   import askopenfilename        # get standard dialogs
from tkColorChooser import askcolor               # they live in Lib/lib-tk
from tkMessageBox   import askquestion, showerror
from tkSimpleDialog import askfloat

class InstanceButton (Button):
	# button state info could be stashed here, for
	# callback handler to use ...
	def __init__ (self, parent, text, path, **kw):
		Button.__init__(self, parent, kw, text=text, command=self.onSetInstance)
		self.text = text
		self.path = path

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


	def onSetInstance (self):
		"""
		handler for instance button
		update the logTool with log from selected instance
		"""
		print "onSetInstance: " + self.text

		logToolFrame = self.getLogToolFrame()
		if not logToolFrame:
			print "could not find LogToolFrame - bailing"
			return

		logFilePath = self.path + "/logs/catalina.out"
		logToolFrame.pathLabel.config (text=logFilePath)
		logToolFrame.logTool.changePath(logFilePath)
		logToolFrame.update_log_text()

taos_instances = {
	"tomcat/tomcat" : "/Library/Java/Extensions/tomcat/jakarta-tomcat-5.0.16",
	"ani-tomcat" : "/Library/Java/Extensions/tomcat/tomcat-ani"
}

tremor_instances = {
	"devel" : "L:/ostwald/tomcat/tomcat",
	"test" : "L:/ostwald/tomcat/tomcat-test",
	"clean" : "L:/ostwald/tomcat/tomcat-clean",
	"preview" : "L:/preview/ostwald/tomcat/tomcat-preview"
}

bolide_instances = {}

def add_instance (dcsInstance, instances):
	instances[dcsInstance.name] = dcsInstance.path

def get_instances ():
	host = os.getenv ("HOST")
	platform = sys.platform
	print "\thost: %s\n\tplatform %s" % (os.getenv ("HOST"), sys.platform)
	instances = {}
	if host and host.find ("bolide")!= -1:
		bolide_instance_path = "/export/services/dcs/dcs.dlese.org/tomcat"
		walker = InstanceWalker (bolide_instance_path)
		for instance in walker.instances:
			instances [instance.displayname] = instance.path
		return instances
	else:
		return tremor_instances
	

if __name__ == "__main__":
	root = Tk()
	instances = get_instances()
	for instance in instances.keys():
		InstanceButton (root, instance, instances[instance], padx=10).pack(side=LEFT)

	root.mainloop()
