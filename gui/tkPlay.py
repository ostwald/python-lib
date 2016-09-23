from Tkinter import *
from tkMessageBox import *
from sys import stdout, exit

class MyButton(Button):
	def __init__(self, parent=None, **config):		   # add callback method
		Button.__init__(self, parent, config)		   # and pack myself
		self.pack()
		self.config(command=self.callback)
	def callback(self):								   # default press action
		print 'Goodbye world...'					   # replace in subclasses
		self.quit()

class MyFrame(Frame):                            # an extended Frame
    def __init__(self, parent=None):
        Frame.__init__(self, parent)           # do superclass init
        self.pack(fill=BOTH)
        self.data = 42
        self.make_widgets()                    # attach widgets to self
    def make_widgets(self):
        widget = MyButton(self, text='Hello frame world!', command=self.message)
        widget.pack(side=TOP, expand=NO)
    def message(self):
        self.data = self.data + 1
        print 'Hello frame world %s!' % self.data

def myWindow ():
	root = Tk()
	root.title ('my window')
	frame = MyFrame(root)
	frame.pack (fill=BOTH, expand=YES)
	frame.config (bg="#cc99ff")
	mainloop()
if __name__ == '__main__':
	# button1 = MyButton(text='Hello subclass world').mainloop()
	# myWindow()

	def callback():
		if askyesno('Verify', 'Do you really want to quit?'):
			showwarning('Yes', 'Quit not yet implemented')
		else:
			showinfo('No', 'Quit has been cancelled')

	errmsg = 'Sorry, no Spam allowed!'
	Button(text='Quit', command=callback).pack(fill=X)
	Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
	mainloop()
	
