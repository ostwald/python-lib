# define a name:callback demos table
from Tkinter import *              # get base widget set
from tkFileDialog   import askdirectory        # get standard dialogs


class OpenButton:
	def __init__ (self, parent):
		self.path = None
		self.parent = parent
		Button (parent, text="Select a Directory", command=self.get_path).pack()

	def get_path (self):
		ret = askdirectory(initialdir="/Users/ostwald")
		if ret:
			self.path = ret
		else:
			self.path = None
		self.parent.quit()

def tester ():
	root = Tk()
	button = OpenButton (root)
	root.mainloop()
	print "button value: " + button.path

if __name__ == "__main__":
	tester()
	
	import Tkinter, tkFileDialog

# dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

