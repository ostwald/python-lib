#############################################
# a quit button that verifies exit requests;
# to reuse, attach an instance to other guis
#############################################

from Tkinter import *						   # get widget classes
from tkMessageBox import askokcancel		   # get canned std dialog

class Quitter(Frame):

	confirm = 0
	
	def __init__(self, parent=None, text='Quit'):		   # constructor method
		Frame.__init__(self, parent)
		self.pack()
		if self.confirm:
			command=self.quit
		else:
			command = self.quit_now
		widget = Button(self, text=text, command=command)
		widget.pack(expand=YES, fill=BOTH, side=LEFT)
	def quit(self):
		ans = askokcancel('Verify exit', "Really quit?")
		if ans: Frame.quit(self)
	def quit_now (self):
		self.master.quit()

if __name__ == '__main__':	Quitter().mainloop()

