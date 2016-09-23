"""
a start at a tool to let users create filters. but right now it just puts up a
single entry
"""

import sys
if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")
	
from Tkinter import *
from gui.quitter import Quitter

def fetch():
    print 'Input => "%s"' % ent.get()              # get text

root = Tk()
ent = Entry(root)
ent.insert(0, 'Type words here')                   # set text
ent.pack(side=TOP, fill=X, padx=10, pady=10)                         # grow horiz

ent.focus()                                        # save a click
ent.bind('<Return>', (lambda event: fetch()))      # on enter key
btn = Button(root, text='Fetch', command=fetch)    # and on button 
btn.pack(side=LEFT)
Quitter(root).pack(side=RIGHT)
root.mainloop()
