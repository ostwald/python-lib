import sys
if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from Tkinter import *			   # get base widget set
from DashButtons import DashButton, demos, general_buttons, instance_buttons
from gui.quitter import Quitter		   # attach a quit object to me


class DemoContainer (Frame):
	def __init__(self, parent=None, name="Demo Container"):
		Frame.__init__(self, parent)
		self.name = name

		self.pack()
		Label(self, text=self.name).pack()
		for (key, value) in demos.items():
			Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)

class ContainerLabel (Label):
	def __init__ (self, parent, text):
		Label.__init__(self, parent, text=text)
		self.config (bg = "gray")
		self.pack ()

class DcsContainer (Frame):
	def __init__(self, parent=None, name="Dash Container", buttons=[]):
		Frame.__init__(self, parent)
		self.name = name
		self.buttons = []

		self.pack()
		ContainerLabel(self, text=self.name)
		## Label(self, text=self.name)
		for (key, value) in buttons.items():
			dashButton = DashButton(self, text=key, command=value)
			self.buttons.append (dashButton)
			dashButton.pack(side=LEFT, fill=BOTH)


class DashBoard:
	def __init__(self, parent=None, name="Dash Container"):
		root = Tk()
		root.title ("DCS Dash Board")
		self.name = name
		self.buttons = []

		
		Label(root, text=("DCS Dash Board")).pack()
		DcsContainer(root, "General Tools", general_buttons)
		DcsContainer(root, "Instance Tools", instance_buttons)
		DemoContainer(root)
		Quitter(root).pack(side=TOP, fill=BOTH) 
		root.mainloop()
			  
if __name__ == '__main__':
	DashBoard ()
